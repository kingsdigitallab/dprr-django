from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# from promrep.forms import PromrepFacetedSearchForm
from promrep.models import PostAssertion, Person
from promrep.forms import PromrepFacetedSearchForm
from promrep.solr_backends.solr_backend_field_collapsing import GroupedSearchQuerySet

import promrep.views as views

sqs = GroupedSearchQuerySet().models(PostAssertion).group_by('person_uniq_link')

urlpatterns = patterns('', url(r'^$',
                               views.PromrepFacetedSearchView(
                                   form_class=PromrepFacetedSearchForm,
                                   load_all=True,
                                   searchqueryset=sqs),
                               name='bijagos_haystack_search')
            )

urlpatterns += patterns('',
                        url(r'^person/(?P<person_id>[0-9]+)/$',
                               views.person_detail,
                               name='person_detail'),
                       )
