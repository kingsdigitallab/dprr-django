from .base import *  # noqa

DEBUG = True

INTERNAL_IPS = (
    "dprr-dev.dighum.kcl.ac.uk",
    "137.73.123.239",
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "app_dprr_dev",
        "USER": "app_dprr",
        "PASSWORD": "",
        "HOST": "",
    }
}

LOGGING_LEVEL = logging.DEBUG  # noqa

LOGGING["loggers"]["django"]["level"] = LOGGING_LEVEL  # noqa
LOGGING["loggers"]["django_auth_ldap"]["level"] = LOGGING_LEVEL  # noqa
LOGGING["loggers"]["promrep"]["level"] = LOGGING_LEVEL  # noqa

# -----------------------------------------------------------------------------
# Development Installed Applications Settings
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Haystack Config
# -----------------------------------------------------------------------------

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.solr_backend.SolrEngine",
        "URL": "http://127.0.0.1:8182/solr",
    },
}

# for docker if using
# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': ('promrep.solr_backends.'
#                    'solr_backend_field_collapsing.GroupedSolrEngine'),
#         'URL': 'http://solr:8983/solr/dprr',
#         # Assuming you created a core named 'tester' as described in
#         # installing search engines.
#         'ADMIN_URL': 'http://127.0.0.1:8983/solr/admin/cores'
#         # ...or for multicore...
#         # 'URL': 'http://127.0.0.1:8983/solr/mysite',
#     },
# }


# -----------------------------------------------------------------------------
# Django Extensions
# http://django-extensions.readthedocs.org/en/latest/
# -----------------------------------------------------------------------------

try:
    import django_extensions  # noqa

    INSTALLED_APPS = INSTALLED_APPS + ("django_extensions",)  # noqa
except ImportError:
    pass

# -----------------------------------------------------------------------------
# Django Debug Toolbar
# http://django-debug-toolbar.readthedocs.org/en/latest/
# -----------------------------------------------------------------------------

# try:
#     import debug_toolbar  # noqa
#
#     INSTALLED_APPS = INSTALLED_APPS + ("debug_toolbar",)
#     MIDDLEWARE_CLASSES += (  # noqa
#         "debug_toolbar.middleware.DebugToolbarMiddleware",
#     )
#     DEBUG_TOOLBAR_PATCH_SETTINGS = False
#
#     DEBUG_TOOLBAR_PANELS = [
#         "debug_toolbar.panels.versions.VersionsPanel",
#         "debug_toolbar.panels.timer.TimerPanel",
#         "debug_toolbar.panels.settings.SettingsPanel",
#         "debug_toolbar.panels.headers.HeadersPanel",
#         "debug_toolbar.panels.request.RequestPanel",
#         "debug_toolbar.panels.sql.SQLPanel",
#         "debug_toolbar.panels.staticfiles.StaticFilesPanel",
#         "debug_toolbar.panels.templates.TemplatesPanel",
#         "debug_toolbar.panels.cache.CachePanel",
#         "debug_toolbar.panels.signals.SignalsPanel",
#         "debug_toolbar.panels.logging.LoggingPanel",
#         "debug_toolbar.panels.redirects.RedirectsPanel",
#     ]
#
# except ImportError:
#     pass


# -----------------------------------------------------------------------------
# Django Haystack Panel
# https://github.com/streeter/django-haystack-panel
# -----------------------------------------------------------------------------

try:
    import haystack_panel  # noqa

    INSTALLED_APPS = INSTALLED_APPS + ("haystack_panel",)
    DEBUG_TOOLBAR_PANELS.append("haystack_panel.panel.HaystackDebugPanel")

except ImportError:
    pass

# -----------------------------------------------------------------------------
# Local settings
# -----------------------------------------------------------------------------

try:
    from .local import *  # noqa
except ImportError:
    print("failed to import local settings")

    from .test import *  # noqa

    print("the project is running with test settings")
    print("please create a local settings file")
