#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Django settings for DPRR project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/

For production settings see
https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
"""

from wagtailbase import settings as ws

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_NAME = 'dprr'
PROJECT_TITLE = 'Digitising the Prosopography of the Roman Republic'

#------------------------------------------------------------------------------
# Core Settings
# https://docs.djangoproject.com/en/1.6/ref/settings/#id6
#------------------------------------------------------------------------------

ADMINS = (
    ('Luis Figueira', 'luis.figueira@kcl.ac.uk'),
)
MANAGERS = ADMINS

ALLOWED_HOSTS = []

# https://docs.djangoproject.com/en/1.6/ref/settings/#caches
# https://docs.djangoproject.com/en/dev/topics/cache/
# http://redis.io/topics/lru-cache
# http://niwibe.github.io/django-redis/
CACHE_REDIS_DATABASE = '1'

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:' + CACHE_REDIS_DATABASE,
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True
        }
    }
}


# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'south',
)

INSTALLED_APPS += ws.INSTALLED_APPS

INSTALLED_APPS += (
    'promrep',
    'wagtailbase',
)

INTERNAL_IPS = ('127.0.0.1',)

# https://docs.djangoproject.com/en/1.6/topics/logging/
LOGGING_ROOT = os.path.join(BASE_DIR, 'logs')
LOGGING_LEVEL = 'WARN'

if not os.path.exists(LOGGING_ROOT):
    os.makedirs(LOGGING_ROOT)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(levelname)s %(asctime)s %(module)s '
                       '%(process)d %(thread)d %(message)s')
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'django.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': LOGGING_LEVEL,
            'propagate': True,
        },
    },
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

MIDDLEWARE_CLASSES += ws.MIDDLEWARE_CLASSES

ROOT_URLCONF = PROJECT_NAME + '.urls'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'))

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = False
USE_TZ = True

WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'


#------------------------------------------------------------------------------
# Authentication
# https://docs.djangoproject.com/en/1.6/ref/settings/#auth
#------------------------------------------------------------------------------

LOGIN_URL = 'django.contrib.auth.views.login'
LOGIN_REDIRECT_URL = ''


#------------------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# https://docs.djangoproject.com/en/1.6/ref/settings/#static-files
#------------------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL.strip('/'))

if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'assets'),)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

MEDIA_URL = STATIC_URL + 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL.strip('/'))

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)


#------------------------------------------------------------------------------
# Installed Applications Settings
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# CMS
#------------------------------------------------------------------------------

ITEMS_PER_PAGE = ws.ITEMS_PER_PAGE

#------------------------------------------------------------------------------
# Wagtail
# http://wagtail.readthedocs.org/en/latest/
#------------------------------------------------------------------------------

WAGTAIL_SITE_NAME = PROJECT_TITLE

#------------------------------------------------------------------------------
# Django Grappelli
# http://django-grappelli.readthedocs.org/en/latest/index.html
#------------------------------------------------------------------------------

GRAPPELLI_ADMIN_TITLE = PROJECT_TITLE


#------------------------------------------------------------------------------
# Development Installed Applications Settings
#------------------------------------------------------------------------------

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
# Django Debug Toolbar
# http://django-debug-toolbar.readthedocs.org/en/latest/
#------------------------------------------------------------------------------

try:

    import debug_toolbar

    INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

except ImportError:
    pass


#------------------------------------------------------------------------------
# Local settings
# Ignored in version control to allowing for settings to be defined per machine
#------------------------------------------------------------------------------
try:
    from local_settings import *
except ImportError:
    pass