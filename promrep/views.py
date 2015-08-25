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


        office_options = [ {'value': '', 'label': '--- Please select office name ---', 'is_selected' : False} ]

        if 'office' not in selected_facets.keys():
            office_options[0]['is_selected'] = True

        # TODO: should use facet_counts
        for o in Office.objects.all():
            odict = {'value': 'office:' + o.name, 'label': o.name, 'is_selected' : False}

            if 'office' in selected_facets.keys():
                if selected_facets['office'] == o.name:
                    odict['is_selected'] = True

            office_options.append(odict)

        date_st_options = [ {'value': 'date_st:', 'label': '--- Please select start date ---', 'is_selected' : False}, ]

        if 'date_st' not in selected_facets.keys():
            date_st_options[0]['is_selected'] = True

        # TODO: should use facet_counts
        for d in range(-510, 0, 10):
            ddict = {'value': 'date_st:' + str(d), 'label': d, 'is_selected' : False}

            if 'date_st' in selected_facets.keys():
                if selected_facets['date_st'] == str(d):
                    ddict['is_selected'] = True

            date_st_options.append(ddict)

        # TODO: should go as a separate object
        context['office_options'] = office_options
        context['date_st_options'] = date_st_options

        return context


def person_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    post_assertions = PostAssertion.objects.filter(person=person)

    return render(request, 'promrep/persons/detail.html',
                  {'person': person,
                   'post_assertions': post_assertions})


