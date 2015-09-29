from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.core.validators import RegexValidator

from haystack.forms import FacetedSearchForm

validate_range = RegexValidator(
    r'^-?\d+\s-\s-?\d+$', 'Incorrect format; Please enter range in the format "date_from - date_end", e.g.: "-100 - -80".')


def get_range_parts(value_range):
    """Returns a tuple of start value and end value extracted from
    `value_range`.

    `value_range` should be in the format "<int> - <int>".

    """
    return value_range.split(' - ', 1)


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


class PromrepFacetedSearchForm(FacetedSearchForm):

    """Extends FacetedSearchForm, as we have special requirements in terms of
    facet handling and date filtering."""

    post_date = forms.CharField(
        max_length=13, required=False, validators=[validate_range],
        widget=forms.TextInput(attrs={'placeholder': 'from - to'}))

    range_facet_fields = ['post_date', ]

    def no_query_found(self):
        """Determines the behaviour when no query was found; returns all the
        results."""
        return self.searchqueryset.all()

    def search(self):
        sqs = super(PromrepFacetedSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        # Narrow the search by the ranges of dates
        # Requires, of course, that the form be bound.
        if self.is_bound:
            for field in self.range_facet_fields:
                field_data = self.cleaned_data.get(field)
                if field_data:
                    start, end = get_range_parts(field_data)
                    sqs = sqs.narrow(u'%s:[%s TO %s]' % (field, start, end))

        return sqs
