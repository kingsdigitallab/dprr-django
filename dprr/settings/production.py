#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pickle import FALSE

from .base import *  # noqa
from .base import env

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG",False)
TEMPLATE_DEBUG = False

# Added for backward compatibility with some old migrations
MIDDLEWARE_CLASSES = MIDDLEWARE

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=['dprr-os.kdl.kcl.ac.uk'])

# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# replace this with actual database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("POSTGRES_DB"),
        'USER': env("POSTGRES_USER"),
        'PASSWORD': env("POSTGRES_PASSWORD"),
        'HOST': env("POSTGRES_HOST"),
        'PORT': '5432',
    },
}

# https://github.com/sehmaschine/django-grappelli/issues/456
# Any value other than "" in the setting value will break the inline templates
TEMPLATE_STRING_IF_INVALID = ''
FABRIC_USER = 'ehall'


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'dprr.settings.local.show_toolbar',
}

# -----------------------------------------------------------------------------
# Haystack Config
# -----------------------------------------------------------------------------

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE':
            'haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine',
        'URL': 'http://elasticsearch:9200/',
        'INDEX_NAME': 'dprr_haystack',
    },
}
