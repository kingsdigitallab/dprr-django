from collections import OrderedDict

import pdfkit
from django.conf import settings as s
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.generic.detail import DetailView
from haystack.generic_views import FacetedSearchView, SearchView
from haystack.query import SearchQuerySet
from promrep.forms import (FastiSearchForm, PromrepFacetedSearchForm,
                           SenateSearchForm)
from promrep.models import (Office, Person, PostAssertion, Province,
                            RelationshipAssertion, StatusAssertion)
from wagtail.admin.templatetags.wagtailadmin_tags import querystring


class PromrepFacetedSearchView(FacetedSearchView):
    facet_fields = [
        "gender",
        "nobilis",
        "novus",
        "tribe",
        "patrician",
        "location",
        "offices",
        "life_events",
        "eques",
    ]

    autocomplete_facets = PromrepFacetedSearchForm.AUTOCOMPLETE_FACETS
    form_class = PromrepFacetedSearchForm
    load_all = True
    print_paginate = 200
    pdf_paginate = 10000

    # Person allows us to search people with no assertions
    queryset = SearchQuerySet().models(Person)

    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        if self.request.GET.get("printme"):
            return self.print_paginate
        elif self.request.GET.get("pdf_view"):
            return self.pdf_paginate
        else:
            return self.paginate_by

    def get_queryset(self):
        queryset = super(PromrepFacetedSearchView, self).get_queryset()

        all_facets = self.autocomplete_facets + self.facet_fields
        options = {"size": 10000}
        for facet in all_facets:
            # only return results with a mincount of 1
            # queryset = queryset.facet(facet, sort="index", limit=-1,
            #                           mincount=1)
            queryset = queryset.facet(facet, **options)

        if "order" in self.request.GET and self.request.GET[
            "order"] == "-date":
            return queryset.order_by("uncertain_exact", "-era_order")

        return queryset.order_by("uncertain_exact", "era_order")

    def get_context_data(self, **kwargs):  # noqa
        context = super(PromrepFacetedSearchView, self).get_context_data(
            **kwargs)

        if self.request.GET.getlist("selected_facets"):
            context["selected_facets"] = self.request.GET.getlist(
                "selected_facets")

            # stores all selected offices for later use in search results
            selected_offices = []
            for facet in context["selected_facets"]:
                if "office" in facet:
                    office_name = facet.split(":")[1]
                    selected_offices.append(office_name)
                    office = Office.objects.get(name=office_name)
                    selected_offices.extend(
                        [o.name for o in office.get_descendants()])

            context["selected_offices"] = selected_offices

        qs = self.request.GET.copy()
        context["querydict"] = qs.copy()
        self.paginate_by = 200

        if self.request.GET.get("q"):
            qs.pop("q")

            # always remove the page number
            if "page" in qs:
                qs.pop("page")

            if len(qs):
                url = "?{0}".format(qs.urlencode())
            else:
                url = reverse("person_search")

            context["remove_text_filter"] = url

        context["era_filter"] = _get_date_url_and_filter(
            qs, "person_search", "era_from", "era_to"
        )

        # used to generate the lists for the autocomplete dictionary
        context["autocomplete_facets"] = self.autocomplete_facets

        for afacet in context["autocomplete_facets"]:

            if self.request.GET.get(afacet):
                qs = self.request.GET.copy()
                qs.pop(afacet)

                url = reverse("person_search")

                if len(qs):
                    url = "?{0}".format(qs.urlencode())

                context[afacet] = (url, self.request.GET.get(afacet))

        office_lookups = s.LOOKUPS["offices"]

        # hierarchical facets data
        try:
            magisterial = Office.objects.get(id=office_lookups["magisterial"])
            if magisterial:
                context[
                    "magisterial_office_list"] = magisterial.get_descendants()
        except:
            pass

        try:
            promagistracies = Office.objects.get(
                id=office_lookups["promagistracies"])
            if promagistracies:
                context[
                    "promagistracies_office_list"
                ] = promagistracies.get_descendants()
        except:
            pass

        try:
            priesthoods = Office.objects.get(id=office_lookups["priesthoods"])
            if priesthoods:
                context[
                    "priesthoods_office_list"] = priesthoods.get_descendants()
        except:
            pass

        try:
            non_magisterial = Office.objects.get(
                id=office_lookups["non_magisterial"])
            if non_magisterial:
                context[
                    "non_magisterial_office_list"
                ] = non_magisterial.get_descendants()
        except:
            pass

        try:
            distinctions = Office.objects.get(
                id=office_lookups["distinctions"])
            if distinctions:
                context[
                    "distinctions_office_list"] = (
                    distinctions.get_descendants())
        except:
            pass

        if "facets" in context and "fields" in context["facets"]:
            if "offices" not in context["facets"]["fields"]:
                context.update({"facets": self.get_queryset().facet_counts()})
            if "offices" in context["facets"]["fields"]:
                context["office_fdict"] = dict(
                    context["facets"]["fields"]["offices"])
            if "location" in context["facets"]["fields"]:
                context["province_fdict"] = dict(
                    context["facets"]["fields"]["location"])

        context["province_list"] = Province.objects.all()

        return context


def _get_date_url_and_filter(qs, view_name, field_from, field_to):
    if (field_from or field_to) in qs:
        field_text = None

        if qs.get(field_from) and qs.get(field_to):
            field_text = "{} to {}".format(qs.pop(field_from)[0],
                                           qs.pop(field_to)[0])
        elif qs.get(field_to):
            field_text = "Before {}".format(qs.pop(field_to)[0])
        elif qs.get(field_from):
            field_text = "After {}".format(qs.pop(field_from)[0])

        # always remove the page number
        if "page" in qs:
            qs.pop("page")

        url = reverse(view_name)
        if len(qs):
            url = "?{}".format(qs.urlencode())

        if field_text:
            return (url, field_text)

    return None


class PersonDetailView(DetailView):
    model = Person
    template_name = "promrep/persons/detail.html"

    def get_context_data(self, **kwargs):  # noqa
        context = super(PersonDetailView, self).get_context_data(**kwargs)

        relationships = OrderedDict()

        relationships_qs = RelationshipAssertion.objects.filter(
            person=self.get_object()
        ).order_by("relationship__order", "relationship_number")
        querystring = "?{0}".format(self.request.GET.copy().urlencode())
        if len(querystring) > 1:
            context["querystring"] = querystring

        if "facet_view" in self.request.GET:
            context["facet_view"] = self.request.GET["facet_view"]
        else:
            context["facet_view"] = "person_search"

        for r in relationships_qs:
            if r.relationship not in relationships:
                relationships[r.relationship] = []

            relationships[r.relationship].append(r)

        context["relationships"] = relationships

        return context


def get_pdf(request):
    pdf_url = request.build_absolute_uri()
    pdf_url = pdf_url.replace("/pdf", "")
    if "?" in pdf_url:
        pdf_url = "{}&pdf_view=1".format(pdf_url)
    else:
        pdf_url = "{}?pdf_view=1".format(pdf_url)

    pdf = pdfkit.from_url(pdf_url, False, options=s.PDFKIT_OPTIONS)
    response = HttpResponse(pdf, content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = 'attachment;\
        filename="dprr_search_results.pdf"'

    return response


def get_relationships_network(request, pk):
    network = {}

    try:
        person = Person.objects.get(pk=pk)
        network = _get_relationships_network(person)
    except Person.DoesNotExist:
        network = {"error": "Person with id {} does not exit".format(pk)}

    return JsonResponse(network)


def _get_relationships_network(person):
    nodes = []
    edges = []

    relationships = RelationshipAssertion.objects.filter(person=person)
    for relationship in relationships:
        for person in [relationship.person, relationship.related_person]:
            node = {"id": person.id, "label": person.__unicode__()}

            if node not in nodes:
                nodes.append(node)

        edge = {
            "id": relationship.id,
            "label": relationship.relationship.__unicode__(),
            "source": relationship.person.id,
            "target": relationship.related_person.id,
        }

        if edge not in edges:
            edges.append(edge)

    return {"nodes": nodes, "edges": edges}


class SenateSearchView(SearchView):
    form_class = SenateSearchForm
    queryset = SearchQuerySet().models(StatusAssertion)
    template_name = "search/senate.html"
    pdf_paginate = 10000

    def get_paginate_by(self, queryset):
        if self.request.GET.get("pdf_view"):
            return self.pdf_paginate
        else:
            return self.paginate_by

    def get_queryset(self):
        queryset = super(SenateSearchView, self).get_queryset()
        certainty = None
        if "dating_certainty" in self.request.GET:
            certainty = int(self.request.GET["dating_certainty"])

        if certainty and "senate_date" in self.request.GET:
            #queryset = SearchQuerySet().models(StatusAssertion)
            # queryset = queryset.narrow(
            #     "date:[{0} TO {0}]".format(self.request.GET["senate_date"])
            # )
            if certainty == 1:
                queryset = queryset.filter(date__in=self.request.GET["senate_date"])
        else:
            queryset = queryset.narrow(
                "date:[{0} TO {0}]".format(SenateSearchForm.INITIAL_DATE)
            )



        if certainty is not None and certainty == 3:
            return queryset.order_by("-date_end")

        return queryset.order_by("date_start")

    def get_context_data(self, **kwargs):  # noqa
        context = super(SenateSearchView, self).get_context_data(**kwargs)
        qs = self.request.GET.copy()
        senateForm = context["form"]

        senate_date = SenateSearchForm.INITIAL_DATE
        dating_certainty = SenateSearchForm.INITIAL_DATING_CERTAINTTY

        context["querydict"] = qs.copy()

        if "senate_date" in senateForm.cleaned_data:
            senate_date = senateForm.cleaned_data["senate_date"]
        if "dating_certainty" in senateForm.cleaned_data:
            dating_certainty = senateForm.cleaned_data["dating_certainty"]

        context["dating_certainty"] = str(dating_certainty)
        context["senate_date"] = int(senate_date) * -1
        return context


class FastiSearchView(FacetedSearchView):
    autocomplete_facets = PromrepFacetedSearchForm.AUTOCOMPLETE_FACETS
    facet_fields = ["office", "location"]
    form_class = FastiSearchForm
    queryset = SearchQuerySet().models(PostAssertion)
    template_name = "search/fasti.html"

    def get_queryset(self):
        queryset = super(FastiSearchView, self).get_queryset()
        queryset = self._apply_facets_to_queryset(queryset)

        if "order" in self.request.GET and self.request.GET[
            "order"] == "-date":
            return queryset.order_by(
                "unknown_exact",
                "-date_sort",
                "office_sort",
                "office_name_exact",
            )
        # , "office_name_exact"
        return queryset.order_by(
            "unknown_exact", "date_sort", "office_sort"
        )

    def _apply_facets_to_queryset(self, queryset):
        options = {"size": 10000}
        for facet in self.autocomplete_facets + self.facet_fields:
            # queryset = queryset.facet(facet, sort="index", limit=-1,
            #                           mincount=1)
            queryset = queryset.facet(facet, **options)

        return queryset

    def get_facet_counts(self):
        queryset = SearchQuerySet().models(PostAssertion)
        queryset = self._apply_facets_to_queryset(queryset)

        params = self.request.GET

        if ("date_from" in params and params["date_from"]) or (
                "date_to" in params and params["date_to"]
        ):
            query = "date:[{} TO {}]".format(
                -1 * int(params["date_from"])
                if "date_from" in params and params["date_from"]
                else PromrepFacetedSearchForm.MIN_DATE,
                -1 * int(params["date_to"])
                if "date_to" in params and params["date_to"]
                else PromrepFacetedSearchForm.MAX_DATE,
            )
            queryset = queryset.narrow(query)

        for field in PromrepFacetedSearchForm.AUTOCOMPLETE_FACETS:
            if field in params and params[field]:
                queryset = queryset.narrow(
                    "{}:{}".format(field, params[field]))

        return queryset.facet_counts()

    def get_paginate_by(self, queryset):
        return 100000

    def get_context_data(self, **kwargs):
        context = super(FastiSearchView, self).get_context_data(**kwargs)
        qs = self.request.GET.copy()

        if self.request.GET.getlist("selected_facets"):
            context["selected_facets"] = qs.getlist("selected_facets")

        context["querydict"] = qs.copy()

        if self.request.GET.get("pdf_view"):
            context["pdf_view"] = 1

        context["date_filter"] = _get_date_url_and_filter(
            qs, "fasti_search", "date_from", "date_to"
        )

        # used to generate the lists for the autocomplete dictionary
        context["autocomplete_facets"] = self.autocomplete_facets

        for afacet in context["autocomplete_facets"]:
            if self.request.GET.get(afacet):
                qs = self.request.GET.copy()
                qs.pop(afacet)

                url = reverse("person_search")

                if len(qs):
                    url = "?{0}".format(qs.urlencode())

                context[afacet] = (url, self.request.GET.get(afacet))

        office_lookups = s.LOOKUPS["offices"]

        # hierarchical facets data
        try:
            magisterial = Office.objects.get(id=office_lookups["magisterial"])
            if magisterial:
                context[
                    "magisterial_office_list"] = magisterial.get_descendants()
        except:
            pass

        try:
            promagistracies = Office.objects.get(
                id=office_lookups["promagistracies"])
            if promagistracies:
                context[
                    "promagistracies_office_list"
                ] = promagistracies.get_descendants()
        except:
            pass

        try:
            priesthoods = Office.objects.get(id=office_lookups["priesthoods"])
            if priesthoods:
                context[
                    "priesthoods_office_list"] = priesthoods.get_descendants()
        except:
            pass

        try:
            non_magisterial = Office.objects.get(
                id=office_lookups["non_magisterial"])
            if non_magisterial:
                context[
                    "non_magisterial_office_list"
                ] = non_magisterial.get_descendants()
        except:
            pass

        try:
            distinctions = Office.objects.get(
                id=office_lookups["distinctions"])
            if distinctions:
                context[
                    "distinctions_office_list"] = (
                    distinctions.get_descendants())
        except:
            pass

        context.update({"facets": self.get_queryset().facet_counts()})

        context["office_fdict"] = dict(
            self.get_facet_counts()["fields"]["office"])

        context["province_list"] = Province.objects.all()
        if "facets" in context and "fields" in context[
            "facets"] and "location" in context["facets"]["fields"]:
            context["province_fdict"] = dict(
                context["facets"]["fields"]["location"])

        return context
