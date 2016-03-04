from base import *

DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = 'UliuxjcW6UBgBfdy/mB/DxSEVpW5U7Rj'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db'
    },
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'author',

    'dprr',
    'promrep',
)

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'promrep.solr_backends.solr_backend_field_collapsing.GroupedSolrEngine',
        'URL': 'http://127.0.0.1:8080/solr'
    },
}
