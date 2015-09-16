from django.views.generic.detail import DetailView

from haystack.generic_views import FacetedSearchView

from promrep.forms import PromrepFacetedSearchForm
from promrep.models import PostAssertion, Person
from promrep.solr_backends.solr_backend_field_collapsing import (
    GroupedSearchQuerySet)


class PromrepFacetedSearchView(FacetedSearchView):
    # TODO: check how to set facet.mincount, can facet_fields be declared as a
    # dictionary?
    facet_fields = ['nomen', 'office', 'date_start']
    form_class = PromrepFacetedSearchForm
    load_all = True
    queryset = GroupedSearchQuerySet().models(
        PostAssertion).group_by('person_id')

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
