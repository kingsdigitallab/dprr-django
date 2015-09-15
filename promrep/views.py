from django.shortcuts import render, get_object_or_404

from haystack.generic_views import FacetedSearchView

from promrep.forms import PromrepFacetedSearchForm
from promrep.models import PostAssertion, Person
from promrep.solr_backends.solr_backend_field_collapsing import (
    GroupedSearchQuerySet)


class PromrepFacetedSearchView(FacetedSearchView):
    facet_fields = ['nomen', 'office']
    # facet_fields = ['nomen', 'office', 'date_start', 'date_end']
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


def person_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    post_assertions = PostAssertion.objects.filter(person=person)

    return render(request, 'promrep/persons/detail.html',
                  {'person': person,
                   'post_assertions': post_assertions})
