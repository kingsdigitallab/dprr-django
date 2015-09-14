from django.conf.urls import patterns, url

from promrep.views import person_detail, PromrepFacetedSearchView


urlpatterns = patterns('',
                       url(r'^$',
                           PromrepFacetedSearchView.as_view(),
                           name='bijagos_haystack_search')
                       )

urlpatterns += patterns('',
                        url(r'^person/(?P<person_id>[0-9]+)/$',
                            person_detail,
                            name='person_detail'),
                        )
