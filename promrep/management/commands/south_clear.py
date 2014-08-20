# script adapted from:
# http://mgalgs.github.io/2012/11/01/making-django-app-reset-south-aware.html

from os.path import dirname, basename
from subprocess import check_output
from django.core.management.base import BaseCommand
from south.models import MigrationHistory

class Command(BaseCommand):
    help = "Clear app (with manage.py sqlclear) and south migrations for app"

    def handle(self, *args, **options):
        app_name = args[0]
        printer = Printer()
        # app_name = basename(dirname(app.__file__))
        printer('Clearing ' + app_name)
        cmd = 'python manage.py sqlclear %s | python manage.py dbshell' % app_name
        printer(check_output(cmd, shell=True), verbosity = 2)
        printer('Clearing south migration history for ' + app_name)
        MigrationHistory.objects.filter(app_name__exact=app_name).delete()

class Printer(object):

    def __init__(self, verbosity = 1):
        self.verbosity = int(verbosity)

    def __call__(self, s, verbosity = 1, prefix = '***'):
        if verbosity <= self.verbosity:
            print prefix, s