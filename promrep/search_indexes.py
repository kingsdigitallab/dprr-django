import datetime
from haystack import indexes
from promrep.models import Person, PostAssertion


class PostAssertionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    person = indexes.CharField(model_attr='person')

    person_id = indexes.FacetCharField(model_attr='person_id')

    # person link used in indexe pages
    person_uniq_link = indexes.FacetCharField()

    uncertain = indexes.FacetBooleanField(model_attr='uncertain')
    item_id = indexes.CharField(model_attr='id')
    office = indexes.FacetCharField(model_attr='office__name')

    nomen = indexes.FacetCharField(model_attr = 'person__nomen', default="")
    cognomen = indexes.FacetCharField(model_attr='person__cognomen', default="")

    date_st = indexes.FacetIntegerField()

    def get_model(self):
        return PostAssertion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_person_uniq_link(self, object):
        """A link to the person object, used to display results of grouped facets"""

        person_str = '<a href="/browse/person/' + str(object.person.id) + '">'
        person_str = person_str + object.person.__unicode__() + "</a>"

        return person_str


    def prepare_date_st(self, object):

        # default date_start set to 0
        date_start = 0

        if object.date_start:
            date_start = object.date_start

        return date_start

