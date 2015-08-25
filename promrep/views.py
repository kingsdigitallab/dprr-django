from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from promrep.models import PostAssertion, Person, Office

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

        ### TODO: this should be applied elsewhere, no??
        for f in ['office']:
            self.searchqueryset = self.searchqueryset.facet(f, mincount=1)

        # print context
        self.results = self.results.facet('office')

        selected_facets = {}

        if self.request.GET.getlist('selected_facets'):
            selected_facets_list = self.request.GET.getlist('selected_facets')

            for facet in selected_facets_list:
                if ":" not in facet:
                    continue

                (field, value) = facet.split(":", 1)
                selected_facets[field] = value


        if 'office' not in selected_facets.keys():
            offices = [ {'value': 'office:', 'label': '--- Please select office name ---', 'is_selected' : True}, ]
        else:
            offices = [ {'value': '', 'label': '--- Please select office name ---', 'is_selected' : False} ]

        # TODO: should use facet_counts
        for o in Office.objects.all():
            odict = {'value': 'office:' + o.name, 'label': o.name, 'is_selected' : False}

            if 'office' in selected_facets.keys():
                if selected_facets['office'] == o.name:
                    odict['is_selected'] = True

            offices.append(odict)




        date_array = [i for i in range(-510, 0, 10)]

        context['offices'] = offices
        context['date_array'] = date_array

        return context


def person_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    post_assertions = PostAssertion.objects.filter(person=person)

    return render(request, 'promrep/persons/detail.html',
                  {'person': person,
                   'post_assertions': post_assertions})


