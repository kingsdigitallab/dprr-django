from django.views.generic.detail import DetailView

from haystack.generic_views import FacetedSearchView

from promrep.forms import PromrepFacetedSearchForm
from promrep.models import PostAssertion, Person
from promrep.solr_backends.solr_backend_field_collapsing import (
    GroupedSearchQuerySet)


class PromrepFacetedSearchView(FacetedSearchView):
    # TODO: check how to set facet.mincount, can facet_fields be declared as a
    # dictionary?
    facet_fields = ['patrician', 'nomen', 'cognomen', 'office', 'province', ]
    alpha_facet_fields = ['nomen', 'office', 'province', 'cognomen',]
    form_class = PromrepFacetedSearchForm
    load_all = True
    queryset = GroupedSearchQuerySet().models(
        PostAssertion).group_by('person_id')

    def get_queryset(self):
        queryset = super(PromrepFacetedSearchView, self).get_queryset()

        for facet in self.alpha_facet_fields:
            queryset = queryset.facet(facet, sort='index', limit=-1)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            PromrepFacetedSearchView, self).get_context_data(**kwargs)
        context['querydict'] = self.request.GET

        if self.request.GET.getlist('selected_facets'):
            context['selected_facets'] = self.request.GET.getlist(
                'selected_facets')

        return context


class PersonDetailView(DetailView):
    model = Person
    template_name = 'promrep/persons/detail.html'
