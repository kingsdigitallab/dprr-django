from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView

from haystack.generic_views import FacetedSearchView

from promrep.forms import PromrepFacetedSearchForm
from promrep.models import PostAssertion, Person
from promrep.solr_backends.solr_backend_field_collapsing import (
    GroupedSearchQuerySet)


class PromrepFacetedSearchView(FacetedSearchView):
    # TODO: check how to set facet.mincount, can facet_fields be declared as a
    # dictionary?
    facet_fields = ['cognomen', 'eques', 'f', 'gender', 'n', 'nobilis', 'nomen',
                    'novus', 'office', 'patrician', 'praenomen', 'province', ]
    alpha_facet_fields = [ 'cognomen','nomen', 'office', 'province', ]
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
        if ('post_date_from' or 'post_date_to') in self.request.GET:
            qs = self.request.GET.copy()

            if 'post_date_from' in qs:
                qs.pop('post_date_from')

            if 'post_date_to' in qs:
                qs.pop('post_date_to')

            # always remove the page number
            if 'page' in qs:
                qs.pop('page')

            url = reverse('haystack_search')
            if len(qs):
                url = '?{0}'.format(qs.urlencode())

            date_text = ""
            if self.request.GET.get('post_date_to') and self.request.GET.get('post_date_from'):
                date_text = self.request.GET.get('post_date_from') + " to " + self.request.GET.get('post_date_to')
            elif self.request.GET.get('post_date_to'):
                date_text = "Before " + self.request.GET.get('post_date_to')
            elif self.request.GET.get('post_date_from'):
                date_text = "After " + self.request.GET.get('post_date_from')

            # if neither dates have values
            # no need to print the filter...
            if date_text != "":
                context['post_date_filter'] = (url, date_text)

        return context


class PersonDetailView(DetailView):
    model = Person
    template_name = 'promrep/persons/detail.html'


# class PromrepFacetedSearchView2(PromrepFacetedSearchView):
#     template_name = 'search/search2.html'
    
