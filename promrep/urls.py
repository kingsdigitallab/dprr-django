from django.conf.urls import url
from promrep.views import (FastiSearchView, PersonDetailView,
                           PromrepFacetedSearchView, SenateSearchView,
                           get_relationships_network)
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^person/$', PromrepFacetedSearchView.as_view(),
        name='haystack_search'),
    url(r'^person/(?P<pk>\d+)/$', PersonDetailView.as_view(),
        name='person-detail'),
    url(r'^person/(?P<pk>\d+)/network/$', get_relationships_network,
        name='person-network'),
    url(r'^senate/$', SenateSearchView.as_view(), name='senate_search'),
    url(r'^fasti/$', cache_page(600 * 600)(FastiSearchView.as_view()),
        name='fasti_search')
]
