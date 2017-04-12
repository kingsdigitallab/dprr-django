from collections import OrderedDict

from django.conf import settings as s
from django.core.urlresolvers import reverse

from django.http import JsonResponse, HttpResponse
from django.views.generic.detail import DetailView
from haystack.generic_views import FacetedSearchView, SearchView

from promrep.forms import PromrepFacetedSearchForm, SenateSearchForm
from promrep.models import (Office, Person, PostAssertion, Province,
                            RelationshipAssertion, StatusAssertion)
from promrep.solr_backends.solr_backend_field_collapsing import \
    GroupedSearchQuerySet

import pdfkit


class PromrepFacetedSearchView(FacetedSearchView):
    facet_fields = ['gender', 'nobilis', 'novus', 'tribe',
                    'patrician', 'province', 'offices', 'life_date_types',
                    'eques']

    autocomplete_facets = PromrepFacetedSearchForm.AUTOCOMPLETE_FACETS
    form_class = PromrepFacetedSearchForm
    load_all = True
    print_paginate = 200
    pdf_paginate = 10000

    # Person allows us to search people with no assertions
    queryset = GroupedSearchQuerySet().models(
        PostAssertion,
        StatusAssertion,
        Person,
        RelationshipAssertion).group_by('person_id')

    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        if self.request.GET.get('printme'):
            return self.print_paginate
        elif self.request.GET.get('pdf_view'):
            return self.pdf_paginate
        else:
            return self.paginate_by

    def get_queryset(self):
        queryset = super(PromrepFacetedSearchView, self).get_queryset()
        all_facets = self.autocomplete_facets + self.facet_fields

        for facet in all_facets:
            # only return results with a mincount of 1
            queryset = queryset.facet(
                facet, sort='index', limit=-1, mincount=1)

        selected_facets = self.request.GET.getlist('selected_facets')
        offices = False
        for facet in selected_facets:
            if 'offices' in facet:
                if 'order' in self.request.GET and\
                        self.request.GET['order'] == '-date':
                    queryset = queryset.order_by('-date_start',
                                                 '-date_end')
                    offices = True
                else:
                    queryset = queryset.order_by('date_start',
                                                 'date_end')
                    offices = True
                break
        if offices:
            return queryset
        if 'order' in self.request.GET and\
                self.request.GET['order'] == '-date':
            return queryset.order_by('-era_order')
        else:
            return queryset.order_by('era_order')

    def get_context_data(self, **kwargs):  # noqa
        context = super(
            PromrepFacetedSearchView, self).get_context_data(**kwargs)

        if self.request.GET.getlist('selected_facets'):
            context['selected_facets'] = self.request.GET.getlist(
                'selected_facets')
            # Find all selected offices for later use in search results
            selected_offices = []
            for facet in self.request.GET.getlist('selected_facets'):
                if 'offices' in facet:
                    office_name = facet.replace('offices:', '')
                    selected_offices.append(office_name)
                    # Add Children to the list as well
                    office = Office.objects.get(name=office_name)
                    for child_office in office.get_descendants():
                        selected_offices.append(child_office.name)
                elif 'office' in facet:
                    office_name = facet.replace('office:', '')
                    selected_offices.append(office_name)
                    # Add Children to the list as well
                    office = Office.objects.get(name=office_name)
                    for child_office in office.get_descendants():
                        selected_offices.append(child_office.name)
            context['selected_offices'] = selected_offices

        qs = self.request.GET.copy()
        context['querydict'] = qs.copy()
        self.paginate_by = 200

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

        context['era_filter'] = self._get_date_url_and_filter(
            'era_from', 'era_to')

        context['date_filter'] = self._get_date_url_and_filter(
            'date_from', 'date_to')

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

        office_lookups = s.LOOKUPS['offices']

        # hierarchical facets data
        try:
            magisterial = Office.objects.get(id=office_lookups['magisterial'])
            if magisterial:
                context[
                    'magisterial_office_list'
                ] = magisterial.get_descendants()
        except:
            pass

        try:
            promagistracies = Office.objects.get(
                id=office_lookups['promagistracies'])
            if promagistracies:
                context[
                    'promagistracies_office_list'
                ] = promagistracies.get_descendants()
        except:
            pass

        try:
            priesthoods = Office.objects.get(id=office_lookups['priesthoods'])
            if priesthoods:
                context[
                    'priesthoods_office_list'
                ] = priesthoods.get_descendants()
        except:
            pass

        try:
            non_magisterial = Office.objects.get(
                id=office_lookups['non_magisterial'])
            if non_magisterial:
                context[
                    'non_magisterial_office_list'
                ] = non_magisterial.get_descendants()
        except:
            pass

        try:
            distinctions = Office.objects.get(
                id=office_lookups['distinctions'])
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

    def _get_date_url_and_filter(self, field_from, field_to):
        if (field_from or field_to) in self.request.GET:
            field_text = None

            qs = self.request.GET.copy()

            if qs.get(field_from) and qs.get(field_to):
                field_text = '{} to {}'.format(
                    qs.pop(field_from)[0], qs.pop(field_to)[0])
            elif qs.get(field_to):
                field_text = 'Before {}'.format(qs.pop(field_to)[0])
            elif qs.get(field_from):
                field_text = 'After {}'.format(qs.pop(field_from)[0])

            # always remove the page number
            if 'page' in qs:
                qs.pop('page')

            url = reverse('haystack_search')
            if len(qs):
                url = '?{}'.format(qs.urlencode())

            if field_text:
                return (url, field_text)

        return None


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
        querystring = '?{0}'.format(self.request.GET.copy().urlencode())
        if len(querystring) > 1:
            context['querystring'] = querystring

        for r in relationships_qs:
            if r.relationship not in relationships:
                relationships[r.relationship] = []

            relationships[r.relationship].append(r)

        context['relationships'] = relationships

        return context


def get_pdf(request):
    pdf_url = request.build_absolute_uri()
    pdf_url = pdf_url.replace('/pdf', '')
    if '?' in pdf_url:
        pdf_url = "{}&pdf_view=1".format(pdf_url)
    else:
        pdf_url = "{}?pdf_view=1".format(pdf_url)

    pdf = pdfkit.from_url(pdf_url, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;\
        filename="dprr_search_results.pdf"'

    return response


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


class SenateSearchView(SearchView):
    load_all = True
    form_class = SenateSearchForm
    queryset = GroupedSearchQuerySet().models(
        StatusAssertion).narrow('senator:true').group_by('person_id')
    template_name = 'search/senate.html'

    def get_queryset(self):
        queryset = super(SenateSearchView, self).get_queryset()

        if 'senate_date' in self.request.GET:
            queryset = GroupedSearchQuerySet().models(
                StatusAssertion).narrow('senator:true').group_by('person_id')
        else:
            queryset = queryset.narrow('date:[{0} TO {0}]'.format(
                SenateSearchForm.INITIAL_DATE))
        # queryset = queryset.narrow('uncertain:false')
        certainty = self.request.GET.get('dating_certainty')
        if certainty is not None and certainty == '3':
            return queryset.order_by('-date_end')
        else:
            return queryset.order_by(
                'date_start')

    def get_context_data(self, **kwargs):  # noqa
        context = super(SenateSearchView, self).get_context_data(**kwargs)
        qs = self.request.GET.copy()
        senate_date = SenateSearchForm.INITIAL_DATE_DISPLAY

        context['querydict'] = qs.copy()

        if 'senate_date' in qs:
            senate_date = qs.pop('senate_date')[0]

        context['senate_date'] = senate_date

        return context
