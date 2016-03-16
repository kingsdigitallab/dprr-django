from django.conf.urls import patterns, url

from promrep.views import (PersonDetailView, 
		PromrepFacetedSearchView, PromrepFacetedSearchView2)


urlpatterns = patterns('',
                       url(r'^$',
                           PromrepFacetedSearchView.as_view(),
                           name='haystack_search')
                       )

urlpatterns += patterns('',
                        url(r'^person/(?P<pk>\d+)/$',
                            PersonDetailView.as_view(),
                            name='person-detail'),
                        )

# test url for UI 
urlpatterns += patterns('',
                       url(r'^test/$',
                           PromrepFacetedSearchView2.as_view(),
                           name='haystack_search2')
                       )
