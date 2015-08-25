from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from promrep.models import PostAssertion, Person

from haystack.views import FacetedSearchView

from pprint import pprint

class PromrepFacetedSearchView(FacetedSearchView):

    def create_response(self):
        print "will create the response!"

        res = super(PromrepFacetedSearchView, self).create_response()
        print "created response"

        return res

    def build_page(self):
        print "[DEBUG][PromrepFacetedSearchView] build_page", str(self.results.count())

        paginator = Paginator(self.results, self.results_per_page)
        page_number = self.request.GET.get('page')

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        return (paginator, page)

    # NOTE: future will change to get_context_data
    #       see https://github.com/django-haystack/django-haystack/pull/1130
    def extra_context(self):
        context = super(PromrepFacetedSearchView, self).extra_context()
        print "ALL ABOUT context"

        ### this should be applied elsewhere, no??
        for f in ['office']:
            self.searchqueryset = self.searchqueryset.facet(f, mincount=1)

        # print context
        self.results = self.results.facet('office')

        facet_counts = self.results.facet_counts()

        offices = [o[0] for o in facet_counts['fields']['office']]
        date_array = [i for i in range(-510, 0, 10)]

        print self.request.GET

#        if self.request.GET['selected_facets']:
#            if 'office:' in self.request.GET['selected_facets']:
#                print

        # print self.queryset.facet_counts()
        context['offices'] = offices
        context['date_array'] = date_array

        return context


def person_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    post_assertions = PostAssertion.objects.filter(person=person)

    return render(request, 'promrep/persons/detail.html',
                  {'person': person,
                   'post_assertions': post_assertions})


