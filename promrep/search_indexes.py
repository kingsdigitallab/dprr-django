from haystack import indexes
from promrep.models import PostAssertion


class PostAssertionIndex(indexes.SearchIndex, indexes.Indexable):
    item_id = indexes.CharField(model_attr='id')

    text = indexes.CharField(document=True, use_template=False)

    person = indexes.CharField(model_attr='person', faceted=True)
    person_id = indexes.IntegerField(model_attr='person__id')
    nomen = indexes.CharField(model_attr='person__nomen', faceted=True)
    cognomen = indexes.CharField(model_attr='person__cognomen', faceted=True)

    office = indexes.CharField(model_attr='office__name', faceted=True)
    uncertain = indexes.BooleanField(model_attr='uncertain', faceted=True)

    date_start = indexes.IntegerField(
        model_attr='date_start', default=0, faceted=True)
    date_end = indexes.IntegerField(
        model_attr='date_end', default=0, faceted=True)

    def get_model(self):
        return PostAssertion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
