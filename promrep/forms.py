from django import forms
from django.utils.safestring import mark_safe
from haystack.forms import FacetedSearchForm, SearchForm
from django.core.urlresolvers import reverse


def get_range_parts(value_range):
    """Returns a tuple of start value and end value extracted from
    `value_range`.

    `value_range` should be in the format "<int> - <int>".

    """
    return value_range.split(' - ', 1)


class ModelLinkWidget(forms.Widget):

    """This widget adds a link, to edit the current inline, after the
    inline form fields.
    """

    def __init__(self, obj, attrs=None):
        super(ModelLinkWidget, self).__init__(attrs)
        self.object = obj

    def render(self, name, value, attrs=None):
        edit_url = reverse('admin:%s_%s_change' % (
            self.object._meta.app_label,
            self.object._meta.model_name),
            args=[self.object.id])
        edit_link = '<a href="%s">Edit %s</a>' % \
            (edit_url,
             self.object._meta.verbose_name.lower())

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


class StatusProvincesWidget(forms.Widget):

    def __init__(self, obj, attrs=None):
        super(StatusProvincesWidget, self).__init__(attrs)
        self.object = obj

    def render(self, name, value, attrs=None):
        return self.object.print_provinces()


class PostInlineForm(forms.ModelForm):

    """This form renders a model and adds a link to edit the nested inline
    model. This is useful for inline editing when the nested inline fields are
    not displayed.
    """

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

    """This form renders a model and adds a link to edit the nested inline
    model. This is useful for inline editing when the nested inline fields are
    not displayed."""

    edit_link = forms.CharField(label='Edit', required=False)

    class Meta:
        exclude = ()
        fieldsets = []

    def __init__(self, *args, **kwargs):
        super(PersonInlineForm, self).__init__(*args, **kwargs)

        # instance is always available, it just does or doesn't have pk.
        self.fields['edit_link'].widget = ModelLinkWidget(self.instance)


class RelationshipAssertionInlineForm(forms.ModelForm):

    """This form renders a model and adds a link to edit the nested inline
    model. This is useful for inline editing when the nested inline fields are
    not displayed."""

    edit_link = forms.CharField(label='Edit', required=False)

    class Meta:
        exclude = ()
        fieldsets = []

    def __init__(self, *args, **kwargs):
        super(RelationshipAssertionInlineForm, self).__init__(*args, **kwargs)

        # instance is always available, it just does or doesn't have pk.
        self.fields['edit_link'].widget = ModelLinkWidget(self.instance)


class StatusInlineForm(forms.ModelForm):

    """This form renders a model and adds a link to edit the nested inline
    model. This is useful for inline editing when the nested inline fields are
    not displayed.
    """

    edit_link = forms.CharField(label='Edit', required=False)
    provinces_list = forms.CharField(label='Province(s)', required=False)

    # verbose_name = 'Post'

    class Meta:
        exclude = ()
        fieldsets = []

    def __init__(self, *args, **kwargs):
        super(StatusInlineForm, self).__init__(*args, **kwargs)

        # instance is always available, it just does or doesn't have pk.
        self.fields['edit_link'].widget = ModelLinkWidget(self.instance)
        self.fields['provinces_list'].widget = StatusProvincesWidget(
            self.instance)


class PromrepFacetedSearchForm(FacetedSearchForm):

    """Extends FacetedSearchForm, as we have special requirements in terms of
    facet handling and date filtering."""

    AUTOCOMPLETE_FACETS = ['praenomen', 'nomen', 'cognomen', 're_number',
                           'n', 'f', 'other_names', 'tribe']

    MIN_DATE = -509
    MAX_DATE = -31

    MIN_DATE_FORM = -1 * MAX_DATE
    MAX_DATE_FORM = -1 * MIN_DATE

    era_from = forms.IntegerField(
        required=False, max_value=MAX_DATE_FORM, min_value=MIN_DATE_FORM)
    era_to = forms.IntegerField(
        required=False, max_value=MAX_DATE_FORM, min_value=MIN_DATE_FORM)

    date_from = forms.IntegerField(
        required=False, max_value=MAX_DATE_FORM, min_value=MIN_DATE_FORM)
    date_to = forms.IntegerField(
        required=False, max_value=MAX_DATE_FORM, min_value=MIN_DATE_FORM)

    # class autocomplete is used by the search.js script to select the fields
    # the name of the fields has to match the facet names defined in
    #  views.py
    praenomen = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete', 'title': 'Praenomen'}))
    nomen = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete', 'title': 'Nomen'}))
    cognomen = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete', 'title': 'Cognomen'}))
    re_number = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'title': 'RE'}))
    n = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete', 'title': 'Grandfather'}))
    f = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete', 'title': 'Father'}))
    other_names = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete', 'title': 'Additional Cognomina'}))
    tribe = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'autocomplete', 'title': 'Tribe'}))

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
            data = self.cleaned_data

            era_from = data.get('era_from', None)
            era_to = data.get('era_to', None)

            if era_from or era_to:
                sqs = sqs.narrow(
                    'era:[{} TO {}]'.format(
                        data.get('era_from', self.MIN_DATE) or self.MIN_DATE,
                        data.get('era_to', self.MAX_DATE) or self.MAX_DATE)
                )

            date_from = data.get('date_from', None)
            date_to = data.get('date_to', None)

            if date_from or date_to:
                sqs = sqs.narrow(
                    'date:[{} TO {}]'.format(
                        data.get('date_from', self.MIN_DATE) or self.MIN_DATE,
                        data.get('date_to', self.MAX_DATE) or self.MAX_DATE)
                )

            for field in self.AUTOCOMPLETE_FACETS:
                if data.get(field):
                    sqs = sqs.narrow('{}:{}'.format(field, data.get(field)))

        return sqs

    def clean_era_from(self):
        era_from = self.cleaned_data['era_from']

        if era_from:
            era_from = -1 * era_from

        return era_from

    def clean_era_to(self):
        era_to = self.cleaned_data['era_to']

        if era_to:
            era_to = -1 * era_to

        return era_to

    def clean_date_from(self):
        date_from = self.cleaned_data['date_from']

        if date_from:
            date_from = -1 * date_from

        return date_from

    def clean_date_to(self):
        date_to = self.cleaned_data['date_to']

        if date_to:
            date_to = -1 * date_to

        return date_to


class SenateSearchForm(SearchForm):
    INITIAL_DATE = -180
    INITIAL_DATE_DISPLAY = -1 * INITIAL_DATE

    senate_date = forms.IntegerField(
        required=True, initial=(-1 * INITIAL_DATE),
        max_value=PromrepFacetedSearchForm.MAX_DATE_FORM,
        min_value=PromrepFacetedSearchForm.MIN_DATE_FORM)

    def no_query_found(self):
        return self.searchqueryset.all()

    def search(self):
        sqs = super(SenateSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if self.is_bound:
            data = self.cleaned_data

            senate_date = data.get('senate_date', None)

            if senate_date:
                sqs = sqs.narrow('date:[{0} TO {0}]'.format(
                    data.get('senate_date')))

        return sqs

    def clean_senate_date(self):
        senate_date = self.cleaned_data['senate_date']

        if senate_date:
            senate_date = -1 * senate_date
        else:
            senate_date = self.INITIAL_DATE

        return senate_date
