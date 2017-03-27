import re

from django.conf import settings as s
from django.db.models import Q
from haystack import indexes
from promrep.forms import PromrepFacetedSearchForm, SenateSearchForm
from promrep.models import (
    Office, PostAssertion, RelationshipAssertion, StatusAssertion, Person
)


class MultiValueIntegerField(indexes.MultiValueField):
    field_type = 'integer'

    def convert(self, value):
        if value is None:
            return None
        return list([int(x) for x in value])


class AssertionIndex(indexes.SearchIndex, indexes.Indexable):
    # generic class for shared functions
    text = indexes.CharField(document=True, use_template=True)
    person = indexes.CharField(model_attr='person', faceted=True)
    person_id = indexes.IntegerField(model_attr='person__id')
    dprr_id = indexes.CharField(model_attr='person__dprr_id', null=True)

    praenomen = indexes.MultiValueField(faceted=True, null=True)
    nomen = indexes.MultiValueField(faceted=True, null=True)

    f = indexes.MultiValueField(model_attr='person__f',
                                faceted=True, null=True)
    n = indexes.MultiValueField(model_attr='person__n',
                                faceted=True, null=True)

    re_number = indexes.CharField(model_attr='person__re_number',
                                  faceted=True, null=True)

    cognomen = indexes.MultiValueField(faceted=True, null=True)

    other_names = indexes.MultiValueField(faceted=True, null=True)

    gender = indexes.CharField(
        model_attr='person__sex__name', faceted=True, null=True)
    patrician = indexes.BooleanField(
        model_attr='person__patrician', default=False, faceted=True)
    novus = indexes.BooleanField(
        model_attr='person__novus', default=False, faceted=True)
    nobilis = indexes.BooleanField(
        model_attr='person__nobilis', default=False, faceted=True)

    tribe = indexes.MultiValueField(faceted=True)

    era = MultiValueIntegerField(faceted=True)
    era_order = indexes.IntegerField()

    date_start = indexes.IntegerField(null=True)
    date_end = indexes.IntegerField(null=True)

    def prepare_date_start(self, object):
        return None

    def prepare_date_end(self, object):
        return None

    # used to display the highest office achieved in the search page
    highest_office = indexes.CharField(faceted=False)

    def get_model(self):
        # implemented in the specific facets
        pass

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
        return re.sub(r'[\?\[\]\(\)]', '', value)

    def prepare_cognomen(self, object):
        """The list of cognomens to filter on should not show parentheses or
        brackets."""

        cognomen = object.person.cognomen.strip()
        cognomen = self._clean_name(cognomen)

        return object.person._split_name(cognomen)

    def prepare_other_names(self, object):
        return object.person._split_name(object.person.other_names_plain)

    def prepare_tribe(self, object):
        return list(set(object.person.tribes.values_list('name', flat=True)))

    def prepare_era(self, object):
        """range of dates for the era"""
        person = object.person
        start = PromrepFacetedSearchForm.MIN_DATE
        end = PromrepFacetedSearchForm.MAX_DATE

        if person.era_from:
            start = person.era_from

        if person.era_to:
            end = person.era_to

        res = range(start, end + 1, 1)

        return res

    def prepare_era_order(self, object):
        person = object.person
        start = PromrepFacetedSearchForm.MIN_DATE

        if person.era_from:
            start = person.era_from

        return start

    def prepare_highest_office(self, object):
        """returns a string with the highest office/date a specific person
        archived"""

        return object.person.highest_office


class PostAssertionIndex(AssertionIndex):
    # TODO: remove; deprecated?
    office = indexes.FacetMultiValueField()
    offices = indexes.FacetMultiValueField()

    uncertain = indexes.BooleanField(model_attr='uncertain', faceted=True)

    province = indexes.MultiValueField(faceted=True)
    date = MultiValueIntegerField(faceted=True)
    # date_start = indexes.IntegerField(model_attr='date_start', null=True)
    # date_end = indexes.IntegerField(model_attr='date_end', null=True)

    def prepare_date_start(self, object):
        return object.date_start

    def prepare_date_end(self, object):
        return object.date_end

    life_date_types = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return PostAssertion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""

        return self.get_model().objects.all().exclude(
            Q(date_start__isnull=True) & Q(date_end__isnull=True))

    def prepare_province(self, object):
        # hierarchical facet

        return [pp.name
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
        res = range(start, end + 1, 1)

        return res

    def prepare_office(self, object):
        # Hierarquical facet
        return [o.name for o in object.office.get_ancestors(include_self=True)]

    def prepare_offices(self, object):
        # we don't want any senator post assertions
        # these should all be recorded as Status assertions instead
        # see: https://jira.dighum.kcl.ac.uk/browse/DPRR-256

        olist = object.person.post_assertions

        if object.date_start:
            olist = olist.exclude(date_start__lt=object.date_start)

        if object.date_end:
            olist = olist.exclude(date_end__gt=object.date_end)

        # This is how it was done before... not going to mess with it.
        try:
            senator_offices = Office.objects.get(
                name='senator').get_descendants(include_self=True)
            sen_q = Q(office__in=senator_offices)

            if sen_q:
                olist = olist.exclude(sen_q)
        except:
            pass

        olist = olist.values_list('office__id', flat=True)

        # list of Office objects
        olist = [Office.objects.get(id=o) for o in list(set(olist))]

        return [o.name
                for off in olist
                for o in off.get_ancestors(include_self=True)]

    def prepare_life_date_types(self, object):
        date_types = ['birth', 'exiled', 'restored', 'proscribed',
                      'expelled from Senate']
        relationship_types = {'adopted son of': 'adopted'}

        life_dates = list(set(
            object.person.dateinformation_set.filter(
                date_type__name__in=date_types).values_list(
                    'date_type__name', flat=True)
        ))

        if object.person.dateinformation_set.filter(
            date_type__name='death').exclude(
                date_type__name='death - violent').count() > 0:
            life_dates.append('death')
            life_dates.append('death - other')

        if object.person.dateinformation_set.filter(
                date_type__name='death - violent').count() > 0:
            life_dates.append('death')
            life_dates.append('death - violent')

        for relationship in relationship_types.keys():
            relationships = object.person.relationships_as_subject.filter(
                relationship__name=relationship).count()
            if relationships > 0:
                life_dates.append(relationship_types[relationship])

        return life_dates


class StatusAssertionIndex(AssertionIndex):
    rank = indexes.CharField(model_attr='status__name', faceted=True)
    uncertain = indexes.BooleanField(model_attr='uncertain', faceted=True)
    date = MultiValueIntegerField(faceted=True)
    date_start = indexes.IntegerField(model_attr='date_start', null=True)
    date_start_uncertain = indexes.BooleanField(
        model_attr='date_start_uncertain', default=False)
    date_end = indexes.IntegerField(model_attr='date_end', null=True)
    date_end_uncertain = indexes.BooleanField(
        model_attr='date_end_uncertain', default=False)
    date_display = indexes.CharField()

    senator = indexes.BooleanField(faceted=True, default=False)
    eques = indexes.BooleanField(faceted=True, default=False)

    def get_model(self):
        return StatusAssertion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_date(self, object):
        """range of dates for the post"""

        start = SenateSearchForm.INITIAL_DATE
        end = PromrepFacetedSearchForm.MAX_DATE

        if object.date_start:
            start = object.date_start

        if object.date_end:
            end = object.date_end

        # need to increment the last point
        res = range(start, end + 1, 1)

        return res

    def prepare_senator(self, object):
        return object.status.name.lower() == s.LOOKUPS['status']['senator']

    def prepare_eques(self, object):
        return object.status.name.lower() == s.LOOKUPS['status']['eques']

    def prepare_date_display(self, object):
        return object.print_date()


class RelationshipAssertionIndex(AssertionIndex):

    def get_model(self):
        return RelationshipAssertion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class PersonIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=False)

    person_id = indexes.IntegerField(model_attr='id')
    dprr_id = indexes.CharField(model_attr='dprr_id', null=True)

    praenomen = indexes.MultiValueField(faceted=True, null=True)
    nomen = indexes.MultiValueField(faceted=True, null=True)

    f = indexes.MultiValueField(model_attr='f',
                                faceted=True, null=True)
    n = indexes.MultiValueField(model_attr='n',
                                faceted=True, null=True)

    re_number = indexes.CharField(model_attr='re_number',
                                  faceted=True, null=True)

    cognomen = indexes.MultiValueField(faceted=True, null=True)

    other_names = indexes.MultiValueField(faceted=True, null=True)

    gender = indexes.CharField(
        model_attr='sex__name', faceted=True, null=True)
    patrician = indexes.BooleanField(
        model_attr='patrician', default=False, faceted=True)
    novus = indexes.BooleanField(
        model_attr='novus', default=False, faceted=True)
    nobilis = indexes.BooleanField(
        model_attr='nobilis', default=False, faceted=True)

    tribe = indexes.MultiValueField(faceted=True)

    era = MultiValueIntegerField(faceted=True)
    era_order = indexes.IntegerField()

    def get_model(self):
        return Person

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
        return re.sub(r'[\?\[\]\(\)]', '', value)

    def prepare_cognomen(self, object):
        """The list of cognomens to filter on should not show parentheses or
        brackets."""

        cognomen = object.cognomen.strip()
        cognomen = self._clean_name(cognomen)

        return object._split_name(cognomen)

    def prepare_other_names(self, object):
        return object._split_name(object.other_names_plain)

    def prepare_tribe(self, object):
        return list(set(object.tribes.values_list('name', flat=True)))

    def prepare_era(self, object):
        """range of dates for the era"""
        person = object
        start = PromrepFacetedSearchForm.MIN_DATE
        end = PromrepFacetedSearchForm.MAX_DATE

        if person.era_from:
            start = person.era_from

        if person.era_to:
            end = person.era_to

        res = range(start, end + 1, 1)

        return res

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_era_order(self, object):
        person = object
        start = PromrepFacetedSearchForm.MIN_DATE

        if person.era_from:
            start = person.era_from

        return start
