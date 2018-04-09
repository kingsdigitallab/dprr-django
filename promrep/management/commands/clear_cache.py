from django.core.cache import caches
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Clears the current cache'

    def handle(self, *args, **options):
        dprr_cache = caches['default']
        dprr_cache.clear()
