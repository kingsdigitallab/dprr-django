import re

from haystack import indexes
from promrep.forms import PromrepFacetedSearchForm
from promrep.models import PostAssertion, StatusAssertion


class MultiValueIntegerField(indexes.MultiValueField):
    field_type = 'integer'

    def convert(self, value):
        if value is None:
            return None
        return list([int(x) for x in value])


class PostAssertionIndex(indexes.SearchIndex, indexes.Indexable):
    item_id = indexes.CharField(model_attr='id')

    text = indexes.CharField(document=True, use_template=True)

    person = indexes.CharField(model_attr='person', faceted=True)
    person_id = indexes.IntegerField(model_attr='person__id')

    praenomen = indexes.CharField(
        model_attr='person__praenomen__abbrev', faceted=True, null=True)
    nomen = indexes.CharField(faceted=True, null=True)
    f = indexes.CharField(model_attr='person__f', faceted=True, null=True)
    n = indexes.CharField(model_attr='person__n', faceted=True, null=True)
    cognomen = indexes.CharField(faceted=True, null=True)

    gender = indexes.CharField(
        model_attr='person__sex__name', faceted=True, null=True)
    patrician = indexes.BooleanField(
        model_attr='person__patrician', default=False, faceted=True)
    novus = indexes.BooleanField(
        model_attr='person__novus', default=False, faceted=True)
    eques = indexes.BooleanField(
        model_attr='person__eques', default=False, faceted=True)
    nobilis = indexes.BooleanField(
        model_attr='person__nobilis', default=False, faceted=True)

    office = indexes.CharField(model_attr='office__name', faceted=True)
    uncertain = indexes.BooleanField(model_attr='uncertain', faceted=True)

    province = indexes.MultiValueField(faceted=True)
    date = MultiValueIntegerField(faceted=True)

    # used to display the highest office achieved in the search page
    highest_office = indexes.CharField(faceted=False)

    def get_model(self):
        return PostAssertion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

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

    def prepare_province(self, object):
        return [re.sub(
            r'[\?\[\]\(\)]',
            '',
            p.name.strip().capitalize()) for p in object.provinces.all()]

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

    def prepare_highest_office(self, object):
        """returns a string with the highest office/date a specific person
        archived"""

        pa = object.person.post_assertions.all().order_by(
            '-date_end', '-date_end')[0]

        return pa.office.abbrev_name.title() + " " + pa.print_date()


class StatusAssertionIndex(indexes.SearchIndex, indexes.Indexable):
    item_id = indexes.CharField(model_attr='id')

    text = indexes.CharField(document=True, use_template=True)

    person = indexes.CharField(model_attr='person', faceted=True)
    person_id = indexes.IntegerField(model_attr='person__id')

    praenomen = indexes.CharField(
        model_attr='person__praenomen__abbrev', faceted=True, null=True)
    f = indexes.CharField(model_attr='person__f', faceted=True, null=True)
    n = indexes.CharField(model_attr='person__n', faceted=True, null=True)

    gender = indexes.CharField(
        model_attr='person__sex__name', faceted=True, null=True)
    patrician = indexes.BooleanField(
        model_attr='person__patrician', default=False, faceted=True)
    novus = indexes.BooleanField(
        model_attr='person__novus', default=False, faceted=True)
    nobilis = indexes.BooleanField(
        model_attr='person__nobilis', default=False, faceted=True)

    status = indexes.CharField(model_attr='status__name', faceted=True)
    uncertain = indexes.BooleanField(model_attr='uncertain', faceted=True)
    date = MultiValueIntegerField(faceted=True)

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
