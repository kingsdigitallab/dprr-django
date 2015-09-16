from django.conf.urls import patterns, url

from promrep.views import PersonDetailView, PromrepFacetedSearchView


urlpatterns = patterns('',
                       url(r'^$',
                           PromrepFacetedSearchView.as_view(),
                           name='bijagos_haystack_search')
                       )

urlpatterns += patterns('',
                        url(r'^person/(?P<pk>\d+)/$',
                            PersonDetailView.as_view(),
                            name='person-detail'),
                        )
