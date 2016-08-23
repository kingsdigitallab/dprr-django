from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from haystack.generic_views import FacetedSearchView
from promrep.forms import PromrepFacetedSearchForm
from promrep.models import (
    Office, Person, PostAssertion, RelationshipAssertion, StatusAssertion
)
from promrep.solr_backends.solr_backend_field_collapsing import \
    GroupedSearchQuerySet


class PromrepFacetedSearchView(FacetedSearchView):
    facet_fields = ['eques', 'gender', 'nobilis', 'novus',
                    'patrician', 'province', 'office']

    autocomplete_facets = ['praenomen', 'nomen', 'cognomen', 're_number',
                           'province', 'n', 'f', 'other_names']

    form_class = PromrepFacetedSearchForm
    load_all = True
    queryset = GroupedSearchQuerySet().models(
        PostAssertion, StatusAssertion).group_by('person_id')

    def get_initial(self):
        initial = super(PromrepFacetedSearchView, self).get_initial()
        initial['date_from'] = PromrepFacetedSearchForm.MIN_DATE
        initial['date_to'] = PromrepFacetedSearchForm.MAX_DATE

        return initial

    def get_queryset(self):
        queryset = super(PromrepFacetedSearchView, self).get_queryset()
        all_facets = self.autocomplete_facets + self.facet_fields

        for facet in all_facets:
            # only return results with a mincount of 1
            queryset = queryset.facet(
                facet, sort='index', limit=-1, mincount=1)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            PromrepFacetedSearchView, self).get_context_data(**kwargs)
        context['querydict'] = self.request.GET

        if self.request.GET.getlist('selected_facets'):
            context['selected_facets'] = self.request.GET.getlist(
                'selected_facets')

        qs = self.request.GET.copy()
        if self.request.GET.get('q'):
            qs.pop('q')

            # always remove the page number
            if 'page' in qs:
                qs.pop('page')

            if len(qs):
                url = '?{0}'.format(qs.urlencode())
            else:
                url = reverse('haystack_search')

            context['remove_text_filter'] = url

        # handles the special case of range facets
        if ('date_from' or 'date_to') in self.request.GET:
            qs = self.request.GET.copy()

            if 'date_from' in qs:
                qs.pop('date_from')

            if 'date_to' in qs:
                qs.pop('date_to')

            # always remove the page number
            if 'page' in qs:
                qs.pop('page')

            url = reverse('haystack_search')
            if len(qs):
                url = '?{0}'.format(qs.urlencode())

            date_text = ''
            if self.request.GET.get(
                    'date_to') and self.request.GET.get('date_from'):
                date_text = self.request.GET.get(
                    'date_from') + ' to ' + self.request.GET.get(
                    'date_to')
            elif self.request.GET.get('date_to'):
                date_text = 'Before ' + self.request.GET.get('date_to')
            elif self.request.GET.get('date_from'):
                date_text = 'After ' + self.request.GET.get('date_from')

            # if neither dates have values
            #   no need to print the filter...
            if date_text != '':
                context['date_filter'] = (url, date_text)

        # used to generate the lists for the autocomplete dictionary
        context['autocomplete_facets'] = self.autocomplete_facets

        for afacet in context['autocomplete_facets']:

            if self.request.GET.get(afacet):
                qs = self.request.GET.copy()
                qs.pop(afacet)

                url = reverse('haystack_search')

                if len(qs):
                    url = '?{0}'.format(qs.urlencode())

                context[afacet] = (url, self.request.GET.get(afacet))

        # hierarchical facets data
        # TODO: simplify?
        context['office_list'] = Office.objects.all()
        context['office_fdict'] = dict(
            context['facets']['fields']['office'])

        return context


class PersonDetailView(DetailView):
    model = Person
    template_name = 'promrep/persons/detail.html'


def get_relationships_network(request, pk):
    network = {}

    try:
        person = Person.objects.get(pk=pk)
        network = _get_relationships_network(person)
    except Person.DoesNotExist:
        network = {'error': 'Person with id {} does not exit'.format(pk)}

    return JsonResponse(network)


def _get_relationships_network(person):
    nodes = []
    edges = []

    relationships = RelationshipAssertion.objects.filter(person=person)
    for relationship in relationships:
        for person in [relationship.person, relationship.related_person]:
            node = {
                'id': person.id,
                'label': person.__unicode__()
            }

            if node not in nodes:
                nodes.append(node)

        edge = {
            'id': relationship.id,
            'label': relationship.relationship.__unicode__(),
            'source': relationship.person.id,
            'target': relationship.related_person.id,
        }

        if edge not in edges:
            edges.append(edge)

    return {'nodes': nodes, 'edges': edges}
