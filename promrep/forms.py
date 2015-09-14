from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

from haystack.forms import FacetedSearchForm


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

    date_start = forms.IntegerField(required=False)
    date_end = forms.IntegerField(required=False)

    def no_query_found(self):
        """Determines the behaviour when no query was found; returns all the
        results."""
        return self.searchqueryset.all()

    def search(self):
        sqs = super(PromrepFacetedSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['date_start']:
            sqs = sqs.filter(pub_date__gte=self.cleaned_data['date_start'])

        if self.cleaned_data['date_end']:
            sqs = sqs.filter(pub_date__lte=self.cleaned_data['date_end'])

        return sqs
