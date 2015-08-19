from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from promrep.models import PostAssertion, Person

from haystack.views import FacetedSearchView

class PromrepFacetedSearchView(FacetedSearchView):

    def create_response(self):
        print "will create the response!"

        res = super(PromrepFacetedSearchView, self).create_response()

        print "created response"

        return res

    def build_page(self):
        print "[DEBUG] build_page", str(self.results.count())

        paginator = Paginator(self.results, self.results_per_page)
        page_number = self.request.GET.get('page')

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        return (paginator, page)




def person_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    post_assertions = PostAssertion.objects.filter(person=person)

    return render(request, 'promrep/persons/detail.html',
                  {'person': person,
                   'post_assertions': post_assertions})


