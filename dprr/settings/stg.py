from base import *

CACHE_REDIS_DATABASE = '2'
CACHES['default']['LOCATION'] = '127.0.0.1:6379:' + CACHE_REDIS_DATABASE

INTERNAL_IPS = ('dprr-stg.dighum.kcl.ac.uk', '137.73.123.239',)
ALLOWED_HOSTS = ['dprr-stg.dighum.kcl.ac.uk']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app_dprr_stg',
        'USER': 'app_dprr',
        'PASSWORD': '',
        'HOST': '',
    }
}

#------------------------------------------------------------------------------
# Django Extensions
# http://django-extensions.readthedocs.org/en/latest/
#------------------------------------------------------------------------------

try:
    import django_extensions
    INSTALLED_APPS = INSTALLED_APPS + ('django_extensions',)
except ImportError:
    pass



#------------------------------------------------------------------------------
# Local settings
#------------------------------------------------------------------------------

try:
    from local import *
except ImportError:
    pass
