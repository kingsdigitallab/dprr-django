import datetime
from haystack import indexes
from promrep.models import Person, PostAssertion


class PostAssertionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    person = indexes.CharField(model_attr='person')

    person_id = indexes.FacetCharField(model_attr='person_id')
    person_uniq_link = indexes.FacetCharField()

    item_id =  indexes.CharField(model_attr='id')

    office = indexes.FacetCharField(model_attr='office__name')

    def get_model(self):
        return PostAssertion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


    def prepare_person_uniq_link(self, object):

        person_str = '<a href="/browse/person/' + str(object.person.id) + '">'
        person_str = person_str + object.person.__unicode__() + "</a>"

        return person_str