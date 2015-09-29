#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'UliuxjcW6UBgBfdy/mB/DxSEVpW5U7Rj'

# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# replace this with actual database
DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'app_dprr_local',
         'USER': 'app_dprr',
         'PASSWORD': 'app_dprr',
         'HOST': 'localhost',
         'PORT': '',
    },
}

# https://github.com/sehmaschine/django-grappelli/issues/456
# Any value other than "" in the setting value will break the inline templates
TEMPLATE_STRING_IF_INVALID = '^^^INVALID %s^^^'

def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'dprr.settings.local.show_toolbar',
}

#------------------------------------------------------------------------------
# Haystack Config
#------------------------------------------------------------------------------

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'promrep.solr_backends.solr_backend_field_collapsing.GroupedSolrEngine',
        'URL': 'http://127.0.0.1:8080/solr'
    },
}