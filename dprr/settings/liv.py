from base import *

CACHE_REDIS_DATABASE = '2'
CACHES['default']['LOCATION'] = '127.0.0.1:6379:' + CACHE_REDIS_DATABASE

INTERNAL_IPS = ('dprr.dighum.kcl.ac.uk', '137.73.123.239',)
ALLOWED_HOSTS = ['dprr.dighum.kcl.ac.uk']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app_dprr_liv',
        'USER': 'app_dprr',
        'PASSWORD': '',
        'HOST': '',
    }
}

#------------------------------------------------------------------------------
# Local settings
#------------------------------------------------------------------------------

try:
    from local import *
except ImportError:
    pass