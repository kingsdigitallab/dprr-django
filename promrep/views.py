from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from promrep.models import PostAssertion, Person

def person_index(request):
    person_list = Person.objects.select_related().order_by()
    paginator = Paginator(person_list, 25)

    page = request.GET.get('page')
    office_name = request.GET.get('office')

    try:
        persons = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        persons = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        persons = paginator.page(paginator.num_pages)

    return render_to_response('promrep/persons/index.html',
                              {"office": office_name,
                              "persons": persons,
                               "total_persons": paginator.count})


def person_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    post_assertions = PostAssertion.objects.filter(person=person)

    return render(request, 'promrep/persons/detail.html',
                  {'person': person,
                   'post_assertions': post_assertions})
