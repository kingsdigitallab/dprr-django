from base import *  # noqa

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

# -----------------------------------------------------------------------------
# Local settings
# -----------------------------------------------------------------------------

try:
    from local import *  # noqa
except ImportError:
    pass
