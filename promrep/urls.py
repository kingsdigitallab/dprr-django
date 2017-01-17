from django.conf.urls import patterns, url
from promrep.views import (
    PersonDetailView, PromrepFacetedSearchView, get_relationships_network
)

urlpatterns = patterns('',
                       url(r'^$',
                           PromrepFacetedSearchView.as_view(),
                           name='haystack_search')
                       )

urlpatterns += patterns('',
                        url(r'^person/(?P<pk>\d+)/$',
                            PersonDetailView.as_view(),
                            name='person-detail'),
                        url(r'^person/(?P<pk>\d+)/network/$',
                            get_relationships_network,
                            name='person-network'),
                        )
