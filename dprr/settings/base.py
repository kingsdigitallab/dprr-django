#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Django settings for DPRR project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/

For production settings see
https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
"""

import os

from ddhldap.settings import *  # noqa
from wagtailbase import settings as ws

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..")

PROJECT_NAME = "dprr"
PROJECT_TITLE = "Digitising the Prosopography of the Roman Republic"

# -----------------------------------------------------------------------------
# Core Settings
# https://docs.djangoproject.com/en/1.6/ref/settings/#id6
# -----------------------------------------------------------------------------

ADMINS = ()
MANAGERS = ADMINS

ALLOWED_HOSTS = []

# https://docs.djangoproject.com/en/1.6/ref/settings/#caches
# https://docs.djangoproject.com/en/dev/topics/cache/
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "dprr_cache",
    }
}


# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

INSTALLED_APPS = (
    "grappelli.dashboard",
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "ddhldap",
    "haystack",
    "mptt",
    "django_mptt_admin",
    "author",
)

INSTALLED_APPS += ws.INSTALLED_APPS

INSTALLED_APPS += (
    "ddh_utils",
    "dprr",
    "promrep.apps.PromrepConfig",
    "wagtailbase",
)

INTERNAL_IPS = ("127.0.0.1",)

# https://docs.djangoproject.com/en/1.6/topics/logging/
import logging  # noqa

LOGGING_ROOT = os.path.join(BASE_DIR, "logs")
LOGGING_LEVEL = "WARN"

if not os.path.exists(LOGGING_ROOT):
    os.makedirs(LOGGING_ROOT)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            )
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGGING_ROOT, "django.log"),
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 21,
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "django_auth_ldap": {
            "handlers": ["file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "promrep": {
            "handlers": ["file", "console"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
    },
}

MIDDLEWARE = (
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

MIDDLEWARE += ws.MIDDLEWARE_CLASSES

ROOT_URLCONF = PROJECT_NAME + ".urls"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ""

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.contrib.messages.context_processors.messages",
            ],
            "debug": False,
        },
    },
]


# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/London"
USE_I18N = True
USE_L10N = False
USE_TZ = True

WSGI_APPLICATION = PROJECT_NAME + ".wsgi.application"


# -----------------------------------------------------------------------------
# Authentication
# https://docs.djangoproject.com/en/1.6/ref/settings/#auth
# https://scm.cch.kcl.ac.uk/hg/ddhldap-django
# -----------------------------------------------------------------------------


AUTH_LDAP_REQUIRE_GROUP = "cn=dprr," + LDAP_BASE_OU  # noqa
AUTH_LDAP_USER_FLAGS_BY_GROUP["is_staff"] = "cn=dprr," + LDAP_BASE_OU  # noqa
AUTH_LDAP_USER_FLAGS_BY_GROUP["is_superuser"] = "cn=dprr," + LDAP_BASE_OU  # noqa

LOGIN_URL = "django.contrib.auth.views.login"
LOGIN_REDIRECT_URL = "wagtailadmin_home"


# -----------------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# https://docs.djangoproject.com/en/1.6/ref/settings/#static-files
# -----------------------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL.strip("/"))

if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)

STATICFILES_DIRS = (os.path.join(BASE_DIR, "assets"),)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
)

STATICFILES_FINDERS += ws.STATICFILES_FINDERS

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL.strip("/"))

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)


# -----------------------------------------------------------------------------
# Installed Applications Settings
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# CMS
# -----------------------------------------------------------------------------

ITEMS_PER_PAGE = ws.ITEMS_PER_PAGE

# -----------------------------------------------------------------------------
# Django Compressor
# http://django-compressor.readthedocs.org/en/latest/
# -----------------------------------------------------------------------------

COMPRESS_CSS_FILTERS = ["compressor.filters.cssmin.CSSMinFilter"]

COMPRESS_PRECOMPILERS = ws.COMPRESS_PRECOMPILERS


# -----------------------------------------------------------------------------
# DPRR
# -----------------------------------------------------------------------------

LOOKUPS = {
    "offices": {
        "magisterial": 2,
        "promagistracies": 214,
        "priesthoods": 1,
        "non_magisterial": 210,
        "distinctions": 270,
    },
    "notes": {
        "ruepke_source": "ruepke",
        "date_information_source": "ruepke_LD",
        "post_assertion_source": "ruepke_B",
    },
    "status": {"eques": "eques romanus", "senator": "senator"},
    "dates": {"person_exclude": "attested"},
}

# -----------------------------------------------------------------------------
# Haystack
# -----------------------------------------------------------------------------

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 50

# -----------------------------------------------------------------------------
# Wagtail
# http://wagtail.readthedocs.org/en/latest/
# -----------------------------------------------------------------------------

WAGTAIL_SITE_NAME = PROJECT_TITLE

# -----------------------------------------------------------------------------
# Django Grappelli
# http://django-grappelli.readthedocs.org/en/latest/index.html
# -----------------------------------------------------------------------------

GRAPPELLI_ADMIN_TITLE = PROJECT_TITLE
GRAPPELLI_INDEX_DASHBOARD = "dprr.dashboard.CustomIndexDashboard"

# -----------------------------------------------------------------------------
# Django Author
# https://github.com/lambdalisue/django-author/
# -----------------------------------------------------------------------------

MIDDLEWARE += ("author.middlewares.AuthorDefaultBackendMiddleware",)

AUTHOR_CREATED_BY_FIELD_NAME = "created_by"

# -----------------------------------------------------------------------------
# FABRIC
# -----------------------------------------------------------------------------

FABRIC_USER = ""

# -----------------------------------------------------------------------------
# pdfkit
# -----------------------------------------------------------------------------

PDFKIT_OPTIONS = {
    "page-size": "A4",
    "margin-top": "1.5cm",
    "margin-right": "1.5cm",
    "margin-bottom": "1.5cm",
    "margin-left": "1.5cm",
    "encoding": "UTF-8",
    "print-media-type": "--quiet",
}
