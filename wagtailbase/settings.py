"""
Default setting for wagtail.
http://wagtail.readthedocs.org/en/latest/

In your project settings import these settings and add them to the relevant
sections.
"""

INSTALLED_APPS = (
    'compressor',
    'taggit',
    'modelcluster',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtailsites',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailredirects',
    'wagtail.contrib.wagtailroutablepage',
)

MIDDLEWARE_CLASSES = (
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

STATICFILES_FINDERS = (
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}

ITEMS_PER_PAGE = 10

ALLOW_COMMENTS = True
DISQUS_SHORTNAME = None
