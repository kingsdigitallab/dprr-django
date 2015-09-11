from base import *

DEBUG = True

CACHE_REDIS_DATABASE = '3'
CACHES['default']['LOCATION'] = '127.0.0.1:6379:' + CACHE_REDIS_DATABASE

INTERNAL_IPS = ('dprr-dev.dighum.kcl.ac.uk', '137.73.123.239', )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app_dprr_dev',
        'USER': 'app_dprr',
        'PASSWORD': '',
        'HOST': '',
    }
}

LOGGING_LEVEL = logging.DEBUG

LOGGING['loggers']['django']['level'] = LOGGING_LEVEL
LOGGING['loggers']['django_auth_ldap']['level'] = LOGGING_LEVEL
LOGGING['loggers']['promrep']['level'] = logging.INFO

TEMPLATE_DEBUG = True

#------------------------------------------------------------------------------
# Development Installed Applications Settings
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Haystack Config
#------------------------------------------------------------------------------

HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'ENGINE': 'promrep.solr_backends.solr_backend_field_collapsing.GroupedSolrEngine',
        'URL': 'http://127.0.0.1:8182/solr'
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
    },
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
# Django Debug Toolbar
# http://django-debug-toolbar.readthedocs.org/en/latest/
#------------------------------------------------------------------------------

try:
    import debug_toolbar
    INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]

except ImportError:
    pass


#------------------------------------------------------------------------------
# Local settings
#------------------------------------------------------------------------------

try:
    from local import *
except ImportError:
    print('failed to import local')
    raise ImportError('Error importing local settings')
