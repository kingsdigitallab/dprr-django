from base import *  # noqa

INTERNAL_IPS = ('dprr.dighum.kcl.ac.uk', '137.73.123.239',)
# ALLOWED_HOSTS = ['www.romanrepublic.ac.uk', 'dprr.dighum.kcl.ac.uk',]
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app_dprr_liv',
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
