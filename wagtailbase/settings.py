"""
Default setting for wagtail.
http://wagtail.readthedocs.org/en/latest/

In your project settings import these settings and add them to the relevant
sections.
"""

INSTALLED_APPS = (
    "compressor",
    "taggit",
    "modelcluster",
    "wagtail.core",
    "wagtail.admin",
    "wagtail.documents",
    "wagtail.snippets",
    "wagtail.users",
    "wagtail.images",
    "wagtail.embeds",
    "wagtail.search",
    "wagtail.contrib.redirects",
    "wagtail.contrib.forms",
    "wagtail.sites",
    "wagtail.api",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.table_block",
)

MIDDLEWARE_CLASSES = (

    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
)

STATICFILES_FINDERS = ("compressor.finders.CompressorFinder",)

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

SOUTH_MIGRATION_MODULES = {
    "taggit": "taggit.south_migrations",
}

ITEMS_PER_PAGE = 10

ALLOW_COMMENTS = True
DISQUS_SHORTNAME = None
