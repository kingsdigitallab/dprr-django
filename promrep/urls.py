from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# from promrep.forms import PromrepFacetedSearchForm
from promrep.models import PostAssertion, Person
import promrep.views as views

urlpatterns = patterns('', url(r'^person/(?P<person_id>[0-9]+)/$',
                               views.person_detail,
                               name='person_detail'),
                       )

urlpatterns += patterns('',
                        url(r'^$', views.person_index, name='person_index'),
                        )
