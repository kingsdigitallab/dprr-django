#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
from functools import wraps
from getpass import getuser
from socket import gethostname

from django.conf import settings  # noqa
from fabric.api import cd, env, local, prefix, quiet, require, run, sudo, task
from fabric.colors import green, yellow
from fabric.contrib import django

# put project directory in path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

django.project("dprr")

REPOSITORY = "git@github.com:kingsdigitallab/dprr-django.git"

env.user = settings.FABRIC_USER
env.gateway = "ssh.cch.kcl.ac.uk"
env.hosts = ["dprr.dighum.kcl.ac.uk"]
env.root_path = "/vol/dprr/webroot/"
env.envs_path = os.path.join(env.root_path, "envs")


def server(func):
    """Wraps functions that set environment variables for servers"""

    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            env.servers.append(func)
        except AttributeError:
            env.servers = [func]

        return func(*args, **kwargs)

    return decorated


@task
@server
def dev():
    env.srvr = "dev"
    set_srvr_vars()


@task
@server
def stg():
    env.srvr = "stg"
    set_srvr_vars()


@task
@server
def liv():
    env.srvr = "liv"
    set_srvr_vars()


@task
@server
def localhost():
    """ local server """
    env.srvr = "local"
    env.path = os.path.dirname(os.path.realpath(__file__))
    env.within_virtualenv = "workon dprr"
    env.hosts = [gethostname()]
    env.user = getuser()


@task
@server
def vagrant():
    env.srvr = "vagrant"
    env.path = os.path.join("/", env.srvr)

    # this is necessary because ssh will fail when known hosts keys vary
    # every time vagrant is destroyed, a new key will be generated
    env.disable_known_hosts = True

    env.within_virtualenv = "source {}".format(
        os.path.join("~", "venv", "bin", "activate")
    )

    result = dict(
        line.split() for line in local("vagrant ssh-config", capture=True).splitlines()
    )

    env.hosts = ["%s:%s" % (result["HostName"], result["Port"])]
    env.key_filename = result["IdentityFile"]
    env.user = result["User"]

    print((env.key_filename, env.hosts, env.user))


@task
def unlock():
    """os x servers need to be unlocked"""
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)
    with cd(env.path):
        run("security unlock-keychain")


def set_srvr_vars():
    env.path = os.path.join(env.root_path, env.srvr, "django", "dprr-django")
    env.within_virtualenv = "source {}".format(
        os.path.join(env.envs_path, "dprr-" + env.srvr, "bin", "activate")
    )


@task
def create_virtualenv():
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)
    with quiet():
        env_vpath = os.path.join(env.envs_path, "dprr-" + env.srvr)
        if run("ls {}".format(env_vpath)).succeeded:
            print((green("virtual environment at [{}] exists".format(env_vpath))))
            return

    print((yellow("setting up virtual environment in [{}]".format(env_vpath))))
    run("virtualenv {}".format(env_vpath))


@task
def clone_repo():
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)
    with quiet():
        if run("ls {}".format(os.path.join(env.path, ".git"))).succeeded:
            print((green(("repository at" " [{}] exists").format(env.path))))
            return

    print((yellow("cloning repository to [{}]".format(env.path))))
    run("git clone --recursive {} {}".format(REPOSITORY, env.path))


@task
def setup_environment():
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)
    create_virtualenv()
    clone_repo()
    install_requirements()


@task
def deploy(branch=None, index="yes"):
    update(branch)
    install_requirements()
    # migrate also creates the cache table
    migrate()
    own_django_log()
    collect_static()
    # clear_cache()

    if index.lower() == "yes":
        update_index()

    touch_wsgi()


@task
def update(version=None):
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)

    if version:
        # try specified version first
        to_version = version
    elif not version and env.srvr in ["local", "vagrant", "dev"]:
        # if local, vagrant or dev deploy to develop branch
        to_version = "develop"
    else:
        # else deploy to master branch
        to_version = "master"

    with cd(env.path), prefix(env.within_virtualenv):
        run("git pull")
        run("git checkout {}".format(to_version))


@task
def makemigrations(app=None):
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)

    if env.srvr in ["dev", "stg", "liv"]:
        print((yellow("Do not run makemigrations on the servers")))
        return

    with cd(env.path), prefix(env.within_virtualenv):
        run("./manage.py makemigrations {}".format(app if app else ""))


@task
def migrate(app=None):
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)

    with cd(env.path), prefix(env.within_virtualenv):
        run("./manage.py createcachetable")
        run("./manage.py migrate {}".format(app if app else ""))


@task
def update_index():
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)

    with cd(env.path), prefix(env.within_virtualenv):
        run("./manage.py build_solr_schema > schema.xml")
        run("mv schema.xml ../../solr/collection1/conf/")
        sudo("service tomcat7-{} restart".format(env.srvr))
        run("./manage.py update_index")


@task
def rebuild_index():
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)

    with cd(env.path), prefix(env.within_virtualenv):
        run("./manage.py build_solr_schema > schema.xml")
        run("mv schema.xml ../../solr/collection1/conf/")
        sudo("service tomcat7-{} restart".format(env.srvr))
        run("./manage.py rebuild_index")


@task
def clear_cache():
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)

    with cd(env.path), prefix(env.within_virtualenv):
        run("./manage.py clear_cache")


@task
def collect_static(process=False):
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)

    if env.srvr in ["local", "vagrant"]:
        print((yellow("Do not run collect_static on local servers")))
        return

    with cd(env.path), prefix(env.within_virtualenv):
        run(
            "./manage.py collectstatic {process} --noinput".format(
                process=("--no-post-process" if not process else "")
            )
        )


@task
def install_requirements():
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)

    reqs = "requirements-{}.txt".format(env.srvr)

    try:
        assert os.path.exists(reqs)
    except AssertionError:
        reqs = "requirements.txt"

    with cd(env.path), prefix(env.within_virtualenv):
        run("pip install -U -r {}".format(reqs))


@task
def reinstall_requirement(which):
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)

    with cd(env.path), prefix(env.within_virtualenv):
        run("pip uninstall {0} && pip install --no-deps {0}".format(which))


@task
def own_django_log():
    """ make sure logs/django.log is owned by www-data """

    require("srvr", "path", "within_virtualenv", provided_by=env.servers)

    if env.srvr in ["local", "vagrant"]:
        print((yellow("Do not change ownership of django log on local servers")))
        return
    sudo(
        "chown www-data:www-data {}".format(
            os.path.join(env.path, "logs", "django.log")
        )
    )


@task
def touch_wsgi():
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)

    with cd(os.path.join(env.path, "dprr")), prefix(env.within_virtualenv):
        run("touch wsgi.py")


@task
def command(name=None):
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)

    with cd(env.path), prefix(env.within_virtualenv):
        run("./manage.py {}".format(name if name else ""))


@task
def runserver(port="8000"):
    require("srvr", "path", "within_virtualenv", provided_by=env.servers)

    if env.srvr not in ["local", "vagrant"]:
        print((yellow("this server only runs for development purposes")))
        return

    with cd(env.path), prefix(env.within_virtualenv):
        run("./manage.py runserver 0.0.0.0:{}".format(port))
