import re
from django.conf import settings as s
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from haystack import indexes
from haystack.fields import FacetMultiValueField
from promrep.forms import PromrepFacetedSearchForm, SenateSearchForm
from promrep.models import Office, Person, PostAssertion, StatusAssertion


class MultiValueIntegerField(indexes.MultiValueField):
    field_type = "integer"

    def convert(self, value):
        if value is None:
            return None
        return list([int(x) for x in value])


# For Senate Search
class StatusAssertionIndex(indexes.SearchIndex, indexes.Indexable):
    person = indexes.CharField(model_attr="person", faceted=True)
    rank = indexes.CharField(model_attr="status__name", faceted=True)
    uncertain = indexes.BooleanField(model_attr="uncertain", faceted=True)
    date = MultiValueIntegerField(faceted=True)
    date_start_uncertain = indexes.BooleanField(
        model_attr="date_start_uncertain", default=False
    )
    date_end_uncertain = indexes.BooleanField(
        model_attr="date_end_uncertain", default=False
    )
    date_display = indexes.CharField()
    highest_office = indexes.CharField(faceted=False)

    senator = indexes.BooleanField(faceted=True, default=False)
    text = indexes.CharField(document=True, use_template=False)

    date_start = indexes.IntegerField(null=True)
    date_end = indexes.IntegerField(null=True)

    def get_model(self):
        return StatusAssertion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(
            status__name__iexact=s.LOOKUPS["status"]["senator"]
        )

    def prepare_date(self, object):
        """range of dates for the post"""

        start = SenateSearchForm.INITIAL_DATE
        end = PromrepFacetedSearchForm.MAX_DATE

        if object.date_start:
            start = object.date_start

        if object.date_end:
            end = object.date_end

        # need to increment the last point
        res = list(range(start, end + 1, 1))

        return res

    def prepare_date_start(self, object):
        return object.date_start

    def prepare_date_end(self, object):
        return object.date_end

    def prepare_date_display(self, object):
        return object.print_date()

    def prepare_highest_office(self, object):
        """returns a string with the highest office/date a specific person
        archived"""

        return object.person.highest_office


# For main Person/Browse search page
class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)

    person_id = indexes.IntegerField(model_attr="id")
    dprr_id = indexes.CharField(model_attr="dprr_id", null=True)

    praenomen = indexes.MultiValueField(faceted=True, null=True)
    nomen = indexes.MultiValueField(faceted=True, null=True)
    re_number = indexes.CharField(model_attr="re_number", faceted=True, null=True)
    f = indexes.MultiValueField(model_attr="f", faceted=True, null=True)
    n = indexes.MultiValueField(model_attr="n", faceted=True, null=True)
    tribe = indexes.MultiValueField(faceted=True)
    cognomen = indexes.MultiValueField(faceted=True, null=True)
    other_names = indexes.MultiValueField(faceted=True, null=True)

    era = MultiValueIntegerField(faceted=True)
    era_order = indexes.IntegerField()

    gender = indexes.CharField(model_attr="sex__name", faceted=True, null=True)

    patrician = indexes.BooleanField(
        model_attr="patrician", default=False, faceted=True
    )
    novus = indexes.BooleanField(model_attr="novus", default=False, faceted=True)
    nobilis = indexes.BooleanField(model_attr="nobilis", default=False, faceted=True)
    eques = indexes.BooleanField(faceted=True, default=False)

    life_events = indexes.MultiValueField(faceted=True)

    offices = FacetMultiValueField()
    location = indexes.MultiValueField(faceted=True)
    highest_office = indexes.CharField(faceted=False)

    uncertain = indexes.BooleanField(model_attr="uncertain", faceted=True, null=True)

    def get_model(self):
        return Person

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_praenomen(self, object):
        if not object.praenomen:
            return None

        praenomen = object.praenomen

        if praenomen.has_alternate_name():
            return [praenomen.name, praenomen.alternate_name]

        return praenomen.name

    def prepare_nomen(self, object):
        """The list of nomens to filter on should not show parentheses or
        brackets."""
        nomen = object.nomen.strip()
        nomen = self._clean_name(nomen)

        return object._split_name(nomen)

    def _clean_name(self, value):
        return re.sub(r"[\?\[\]\(\)]", "", value)

    def prepare_tribe(self, object):
        return list(set(object.tribes.values_list("name", flat=True)))

    def prepare_cognomen(self, object):
        """The list of cognomens to filter on should not show parentheses or
        brackets."""

        cognomen = object.cognomen.strip()
        cognomen = self._clean_name(cognomen)

        return object._split_name(cognomen)

    def prepare_other_names(self, object):
        return object._split_name(object.other_names_plain)

    def prepare_era(self, object):
        """range of dates for the era"""
        person = object
        start = PromrepFacetedSearchForm.MIN_DATE
        end = PromrepFacetedSearchForm.MAX_DATE

        if person.era_from:
            start = person.era_from

        if person.era_to:
            end = person.era_to

        res = list(range(start, end + 1, 1))

        return res

    def prepare_era_order(self, object):
        person = object
        start = PromrepFacetedSearchForm.MIN_DATE

        if person.era_from:
            start = person.era_from

        return start

    def prepare_eques(self, object):
        sa_list = StatusAssertion.objects.filter(person=object)
        for sa in sa_list.all():
            if sa.status.name.lower() == s.LOOKUPS["status"]["eques"]:
                return True
        return False

    def prepare_life_events(self, object):
        date_types = [
            "birth",
            "exiled",
            "restored",
            "proscribed",
            "expelled from Senate",
        ]
        relationship_types = {"adopted son of": "adopted"}

        life_dates = list(
            set(
                object.dateinformation_set.filter(
                    date_type__name__in=date_types
                ).values_list("date_type__name", flat=True)
            )
        )

        if (
            object.dateinformation_set.filter(date_type__name="death")
            .exclude(date_type__name="death - violent")
            .count()
            > 0
        ):
            life_dates.append("death")
            life_dates.append("death - other")

        if (
            object.dateinformation_set.filter(date_type__name="death - violent").count()
            > 0
        ):
            life_dates.append("death")
            life_dates.append("death - violent")

        for relationship in list(relationship_types.keys()):
            relationships = object.relationships_as_subject.filter(
                relationship__name=relationship
            ).count()
            if relationships > 0:
                life_dates.append(relationship_types[relationship])

        return life_dates

    def prepare_offices(self, object):
        # we don't want any senator post assertions
        # these should all be recorded as Status assertions instead
        # see: https://jira.dighum.kcl.ac.uk/browse/DPRR-256
        olist = object.post_assertions

        # This is how it was done before... not going to mess with it.
        try:
            senator_offices = Office.objects.get(name="senator").get_descendants(
                include_self=True
            )
            sen_q = Q(office__in=senator_offices)

            if sen_q:
                olist = olist.exclude(sen_q)
        except ObjectDoesNotExist:
            pass

        olist = olist.values_list("office__id", flat=True)

        # list of Office objects
        olist = [Office.objects.get(id=o) for o in list(set(olist))]

        return [o.name for off in olist for o in off.get_ancestors(include_self=True)]

    def prepare_location(self, object):
        # hierarchical facet
        return [
            pp.name
            for pa in object.post_assertions.all()
            for p in pa.provinces.all()
            for pp in p.get_ancestors(include_self=True)
        ]


class PostAssertionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # These offices will be excluded from the queryset
    exclude_offices = ["senator", "senator - office unknown", "princeps senatus"]
    office = FacetMultiValueField()
    office_name = indexes.CharField(model_attr="office__name", faceted=True)
    office_sort = indexes.IntegerField()
    uncertain = indexes.BooleanField(model_attr="uncertain", faceted=True)
    unknown = indexes.BooleanField(model_attr="unknown", faceted=True)
    location = indexes.MultiValueField(faceted=True)
    date = MultiValueIntegerField(faceted=True)
    date_sort = indexes.IntegerField()
    person = indexes.CharField(model_attr="person", faceted=True)
    person_id = indexes.IntegerField(model_attr="person__id")
    dprr_id = indexes.CharField(model_attr="person__dprr_id", null=True)
    person_title = indexes.CharField()

    praenomen = indexes.MultiValueField(faceted=True, null=True)
    nomen = indexes.MultiValueField(faceted=True, null=True)
    f = indexes.MultiValueField(model_attr="person__f", faceted=True, null=True)
    n = indexes.MultiValueField(model_attr="person__n", faceted=True, null=True)
    re_number = indexes.CharField(
        model_attr="person__re_number", faceted=True, null=True
    )
    cognomen = indexes.MultiValueField(faceted=True, null=True)
    other_names = indexes.MultiValueField(faceted=True, null=True)
    tribe = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return PostAssertion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        # Exclude all priesthoods as well
        exclude_offices = self.exclude_offices
        for office in Office.objects.get(name="Priesthoods").get_descendants(
            include_self=True
        ):
            exclude_offices.append(office.name)
        return (
            self.get_model()
            .objects.all()
            .exclude(office__name__in=exclude_offices)
            .exclude(unknown=True)
            .exclude(Q(date_start__isnull=True) & Q(date_end__isnull=True))
            .exclude(date_start__gt=-31)
            .exclude(date_end__gt=-31)
        )

    def prepare_office(self, object):
        # Hierarquical facet
        return [o.name for o in object.office.get_ancestors(include_self=True)]

    # Make a single order integer out of the career tree
    # using tree order (Broughton) + lft
    def prepare_office_sort(self, object):
        # Right now unindexed lists come at the end
        parent_tree_name = object.office.get_root().name
        office_sort = 10000
        if "Magisterial Posts" in parent_tree_name:
            office_sort = 1000
        elif "Distinctions" in parent_tree_name:
            office_sort = 2000
        elif "Promagisterial Posts" in parent_tree_name:
            office_sort = 3000
        elif "Priesthoods" in parent_tree_name:
            office_sort = 4000
        elif "Non-magisterial Posts" in parent_tree_name:
            office_sort = 5000
        office_sort += object.office.lft
        return office_sort

    def prepare_location(self, object):
        # hierarchical facet
        return [
            pp.name
            for p in object.provinces.all()
            for pp in p.get_ancestors(include_self=True)
        ]

    def prepare_date(self, object):
        """range of dates for the post"""
        start = PromrepFacetedSearchForm.MIN_DATE
        end = PromrepFacetedSearchForm.MAX_DATE

        if object.date_start:
            start = object.date_start

        if object.date_end:
            end = object.date_end

        # need to increment the last point
        res = list(range(start, end + 1, 1))

        return res

    def prepare_date_sort(self, object):
        """range of dates for the post"""
        start = PromrepFacetedSearchForm.MIN_DATE

        if object.date_start:
            start = object.date_start

        return start

    def prepare_person_title(self, object):
        """returns a string with the highest office/date a specific person
        archived"""

        person = object.person
        title = "{} {}".format(person.dprr_id, person)
        if person.highest_office:
            title = "{} ({})".format(title, person.highest_office)
        return title

    def prepare_praenomen(self, object):
        if not object.person.praenomen:
            return None

        praenomen = object.person.praenomen

        if praenomen.has_alternate_name():
            return [praenomen.name, praenomen.alternate_name]

        return praenomen.name

    def prepare_nomen(self, object):
        """The list of nomens to filter on should not show parentheses or
        brackets."""

        nomen = object.person.nomen.strip()
        nomen = self._clean_name(nomen)

        return object.person._split_name(nomen)

    def _clean_name(self, value):
        return re.sub(r"[\?\[\]\(\)]", "", value)

    def prepare_cognomen(self, object):
        """The list of cognomens to filter on should not show parentheses or
        brackets."""

        cognomen = object.person.cognomen.strip()
        cognomen = self._clean_name(cognomen)

        return object.person._split_name(cognomen)

    def prepare_other_names(self, object):
        return object.person._split_name(object.person.other_names_plain)

    def prepare_tribe(self, object):
        return list(set(object.person.tribes.values_list("name", flat=True)))
