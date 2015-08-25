from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

from haystack.forms import SearchForm

class ModelLinkWidget(forms.Widget):

    '''This widget adds a link, to edit the current inline, after the inline form fields.'''

    def __init__(self, obj, attrs=None):
        super(ModelLinkWidget, self).__init__(attrs)
        self.object = obj

    def render(self, name, value, attrs=None):
        edit_link = '<a href="../../../%s/%s/%s/">Edit %s</a>' % \
            (self.object._meta.app_label, self.object._meta.object_name.lower(),
             self.object.pk, self.object._meta.verbose_name.lower())

        if self.object.pk:
            return mark_safe(u'%s' % (edit_link))
        else:
            return mark_safe(u'')


class PostAssertionDatesWidget(forms.Widget):

    def __init__(self, obj, attrs=None):
        super(PostAssertionDatesWidget, self).__init__(attrs)
        self.object = obj

    def render(self, name, value, attrs=None):
        return self.object.get_dates()


class PostAssertionProvincesWidget(forms.Widget):

    def __init__(self, obj, attrs=None):
        super(PostAssertionProvincesWidget, self).__init__(attrs)
        self.object = obj

    def render(self, name, value, attrs=None):
        return self.object.print_provinces()


class PostInlineForm(forms.ModelForm):

    '''This form renders a model and adds a link to edit the nested inline
    model. This is useful for inline editing when the nested inline fields are
    not displayed.'''

    edit_link = forms.CharField(label='Edit', required=False)
    print_dates = forms.CharField(label='Post Person Dates', required=False)
    provinces_list = forms.CharField(label='Province(s)', required=False)

    # verbose_name = 'Post'

    class Meta:
        exclude = ()
        fieldsets = []

    def __init__(self, *args, **kwargs):
        super(PostInlineForm, self).__init__(*args, **kwargs)

        # instance is always available, it just does or doesn't have pk.
        self.fields['edit_link'].widget = ModelLinkWidget(self.instance)
        self.fields['print_dates'].widget = PostAssertionDatesWidget(
            self.instance)
        self.fields['provinces_list'].widget = PostAssertionProvincesWidget(
            self.instance)


class PersonInlineForm(forms.ModelForm):

    '''This form renders a model and adds a link to edit the nested inline
    model. This is useful for inline editing when the nested inline fields are
    not displayed.'''

    edit_link = forms.CharField(label='Edit', required=False)

    class Meta:
        exclude = ()
        fieldsets = []

    def __init__(self, *args, **kwargs):
        super(PersonInlineForm, self).__init__(*args, **kwargs)

        # instance is always available, it just does or doesn't have pk.
        self.fields['edit_link'].widget = ModelLinkWidget(self.instance)


class PromrepFacetedSearchForm(SearchForm):
    """reimplements the Faceted Search Form Class, as we have
    special requirements in terms of facet handling"""

    def __init__(self, *args, **kwargs):
        self.selected_facets = kwargs.pop("selected_facets", [])
        super(PromrepFacetedSearchForm, self).__init__(*args, **kwargs)

    def no_query_found(self):
        """
        Determines the behavior when no query was found.
        By default, no results are returned (``EmptySearchQuerySet``).
        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        print "Noqueryfoundstuff"
        print self.__dict__
        print self

        return self.searchqueryset.all()

    def search(self):
        sqs = super(PromrepFacetedSearchForm, self).search()

        # We need to process each facet to ensure that the field name and the
        # value are quoted correctly and separately:
        for facet in self.selected_facets:

            print "selected facets->", facet

            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if field in ["date_st", ]:
                if value:
                    # TODO: review usage of filter vs narrow
                    sqs = sqs.filter(date_st__gt=value)

            else:
                if value:
                    sqs = sqs.narrow(
                        u'%s:"%s"' % (field, sqs.query.clean(value)))

        print "[DEBUG] ", sqs.count()
        print sqs.count()

        print sqs

        return sqs
