import re

from django.db.models import Q
from haystack import indexes
from promrep.forms import PromrepFacetedSearchForm
from promrep.models import (
    Office, PostAssertion, RelationshipAssertion, StatusAssertion
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
    nomen = indexes.CharField(faceted=True, null=True)

    f = indexes.MultiValueField(model_attr='person__f',
                                faceted=True, null=True)
    n = indexes.MultiValueField(model_attr='person__n',
                                faceted=True, null=True)

    re_number = indexes.CharField(model_attr='person__re_number',
                                  faceted=True, null=True)

    other_names = indexes.CharField(
        model_attr='person__other_names_plain', faceted=True, null=True)

    cognomen = indexes.CharField(faceted=True, null=True)

    gender = indexes.CharField(
        model_attr='person__sex__name', faceted=True, null=True)
    patrician = indexes.BooleanField(
        model_attr='person__patrician', default=False, faceted=True)
    novus = indexes.BooleanField(
        model_attr='person__novus', default=False, faceted=True)
    nobilis = indexes.BooleanField(
        model_attr='person__nobilis', default=False, faceted=True)

    tribe = indexes.MultiValueField(faceted=True)

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
        return re.sub(r'[\?\[\]\(\)]', '', nomen)

    def prepare_cognomen(self, object):
        """The list of cognomens to filter on should not show parentheses or
        brackets."""

        cognomen = object.person.cognomen.strip()
        return re.sub(r'[\?\[\]\(\)]', '', cognomen)

    def prepare_tribe(self, object):
        return list(set(object.person.tribes.values_list('name', flat=True)))

    def prepare_highest_office(self, object):
        """returns a string with the highest office/date a specific person
        archived"""

        return object.person.highest_office


class PostAssertionIndex(AssertionIndex):
    # TODO: is this needed?
    # text = indexes.CharField(document=True, use_template=True)

    # TODO: remove; deprecated?
    office = indexes.FacetMultiValueField()
    offices = indexes.FacetMultiValueField()

    uncertain = indexes.BooleanField(model_attr='uncertain', faceted=True)

    province = indexes.MultiValueField(faceted=True)
    date = MultiValueIntegerField(faceted=True)

    life_date_types = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return PostAssertion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""

        return self.get_model().objects.all()

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
        #      see: https://jira.dighum.kcl.ac.uk/browse/DPRR-256

        sen_q = None

        try:
            senator_offices = Office.objects.get(
                name='senator').get_descendants(include_self=True)
            sen_q = Q(office__in=senator_offices)
        except:
            pass

        # flat list of different office ids the person held
        olist = object.person.post_assertions.values_list(
            'office__id', flat=True)

        if sen_q:
            # flat list of different office ids the person held
            olist = object.person.post_assertions.exclude(sen_q).values_list(
                'office__id', flat=True)

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

    senator = indexes.BooleanField(faceted=True, default=False)
    eques = indexes.BooleanField(faceted=True, default=False)

    def get_model(self):
        return StatusAssertion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

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

    def prepare_senator(self, object):
        return object.status.name.lower() == "senator"

    def prepare_eques(self, object):
        return object.status.name.lower() == "eques"


class RelationshipAssertionIndex(AssertionIndex):

    def get_model(self):
        return RelationshipAssertion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
