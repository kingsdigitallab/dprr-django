from collections import OrderedDict

from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from haystack.generic_views import FacetedSearchView
from promrep.forms import PromrepFacetedSearchForm
from promrep.models import (Office, Person, PostAssertion, Province,
                            RelationshipAssertion, StatusAssertion)
from promrep.solr_backends.solr_backend_field_collapsing import \
    GroupedSearchQuerySet


class PromrepFacetedSearchView(FacetedSearchView):
    facet_fields = ['gender', 'nobilis', 'novus', 'tribe',
                    'patrician', 'province', 'offices', 'life_date_types',
                    'eques']

    autocomplete_facets = ['praenomen', 'nomen', 'cognomen', 're_number',
                           'province', 'n', 'f', 'other_names', 'tribe']

    form_class = PromrepFacetedSearchForm
    load_all = True
    queryset = GroupedSearchQuerySet().models(
        PostAssertion,
        StatusAssertion,
        RelationshipAssertion).group_by('person_id')

    def get_queryset(self):
        queryset = super(PromrepFacetedSearchView, self).get_queryset()
        all_facets = self.autocomplete_facets + self.facet_fields

        for facet in all_facets:
            # only return results with a mincount of 1
            queryset = queryset.facet(
                facet, sort='index', limit=-1, mincount=1)

        return queryset

    def get_context_data(self, **kwargs):  # noqa
        context = super(
            PromrepFacetedSearchView, self).get_context_data(**kwargs)

        if self.request.GET.getlist('selected_facets'):
            context['selected_facets'] = self.request.GET.getlist(
                'selected_facets')

        qs = self.request.GET.copy()
        context['querydict'] = qs

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
        try:
            magisterial = Office.objects.get(id=2)
            if magisterial:
                context[
                    'magisterial_office_list'
                ] = magisterial.get_descendants()
        except:
            pass

        try:
            promagistracies = Office.objects.get(id=214)
            if promagistracies:
                context[
                    'promagistracies_office_list'
                ] = promagistracies.get_descendants()
        except:
            pass

        try:
            priesthoods = Office.objects.get(id=1)
            if priesthoods:
                context[
                    'priesthoods_office_list'
                ] = priesthoods.get_descendants()
        except:
            pass

        try:
            non_magisterial = Office.objects.get(id=210)
            if non_magisterial:
                context[
                    'non_magisterial_office_list'
                ] = non_magisterial.get_descendants()
        except:
            pass

        try:
            distinctions = Office.objects.get(id=270)
            if distinctions:
                context[
                    'distinctions_office_list'
                ] = distinctions.get_descendants()
        except:
            pass

        if 'offices' not in context['facets']['fields']:
            context.update({'facets': self.get_queryset().facet_counts()})

        context['office_fdict'] = dict(context['facets']['fields']['offices'])

        context['province_list'] = Province.objects.all()
        context['province_fdict'] = dict(
            context['facets']['fields']['province'])

        return context


class PersonDetailView(DetailView):
    model = Person
    template_name = 'promrep/persons/detail.html'

    def get_context_data(self, **kwargs):  # noqa
        context = super(
            PersonDetailView, self).get_context_data(**kwargs)

        relationships = OrderedDict()

        relationships_qs = RelationshipAssertion.objects.filter(
            person=self.get_object()
        ).order_by('relationship__order', 'relationship_number')

        for r in relationships_qs:
            if r.relationship not in relationships:
                relationships[r.relationship] = []

            relationships[r.relationship].append(r)

        context['relationships'] = relationships

        return context


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
