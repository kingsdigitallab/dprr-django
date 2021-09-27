from django.conf.urls import include, patterns, url
from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailsearch.urls import frontend as wagtailsearch_frontend_urls

urlpatterns = patterns(
    "",
    url(r"^wagtail/", include(wagtailadmin_urls)),
    url(r"^search/", include(wagtailsearch_frontend_urls)),
    url(r"^documents/", include(wagtaildocs_urls)),
    url(r"", include(wagtail_urls)),
)
