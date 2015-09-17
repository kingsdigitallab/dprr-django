from haystack import indexes
from promrep.models import PostAssertion


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

    post_date = indexes.MultiValueField(faceted=True)

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

        return range(start, end, 1)

        return 0
