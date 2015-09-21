from haystack import indexes
from promrep.models import PostAssertion


class MultiValueIntegerField (indexes.MultiValueField):
    field_type = 'integer'

    def convert(self, value):
        if value is None:
            return None
        return list([int(x) for x in value])


class PostAssertionIndex(indexes.SearchIndex, indexes.Indexable):
    item_id = indexes.CharField(model_attr='id')

    text = indexes.CharField(document=True, use_template=False)

    person = indexes.CharField(model_attr='person', faceted=True)
    person_id = indexes.IntegerField(model_attr='person__id')
    nomen = indexes.CharField(model_attr='person__nomen', faceted=True)
    cognomen = indexes.CharField(model_attr='person__cognomen', faceted=True)
    patrician = indexes.BooleanField(
        model_attr='person__patrician', default=False, faceted=True)

    office = indexes.CharField(model_attr='office__name', faceted=True)
    uncertain = indexes.BooleanField(model_attr='uncertain', faceted=True)

    province = indexes.MultiValueField(faceted=True)
    post_date = MultiValueIntegerField(faceted=True)

    def get_model(self):
        return PostAssertion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_post_date(self, object):
        """range of dates for the post"""

        start = -1000
        end = 1000

        if object.date_start:
            start = object.date_start

        if object.date_end:
            end = object.date_end

        # need to increment the last point
        res = range(start, end + 1, 1)

        return res

    def prepare_province(self, object):
        return [p.name for p in object.provinces.all()]
