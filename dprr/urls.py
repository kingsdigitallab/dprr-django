from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.cache import cache_page
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls

from ddhldap.signal_handlers import \
    register_signal_handlers as ddhldap_register_signal_handlers
from promrep.views import (FastiSearchView, PersonDetailView,
                           PromrepFacetedSearchView, SenateSearchView,
                           get_relationships_network)
from promrep.views import get_pdf

ddhldap_register_signal_handlers()

admin.autodiscover()

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pdf/', get_pdf, name='pdf_view'),
    url(r'^browse/senate/$', SenateSearchView.as_view(), name='senate_search'),
    url(r'^browse/fasti/$',
        cache_page(60 * 60 * 24)(FastiSearchView.as_view()),
        name='fasti_search'),
    url(r'^browse/person/$', PromrepFacetedSearchView.as_view(),
        name='person_search'),
    url(r'^browse/person/(?P<pk>\d+)/$', PersonDetailView.as_view(),
        name='person-detail'),
    url(r'^browse/person/(?P<pk>\d+)/network/$', get_relationships_network,
        name='person-network'),

]

try:
    if settings.DEBUG:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]

except ImportError:
    pass

urlpatterns += [
    url(r'^wagtail/', include(wagtailadmin_urls)),
    url(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import os.path

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/',
                          document_root=os.path.join(settings.MEDIA_ROOT,
                                                     'images'))
