from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe


class ModelLinkWidget(forms.Widget):

    '''This widget adds a link, to edit the current inline, after the inline form fields.'''

    def __init__(self, obj, attrs=None):
        super(ModelLinkWidget, self).__init__(attrs)
        self.object = obj

    def render(self, name, value, attrs=None):
        edit_link = '<a href="../../../%s/%s/%s/">Add information to %s</a>' % \
            (self.object._meta.app_label, self.object._meta.object_name.lower(), self.object.pk, self.object._meta.verbose_name.lower())

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


class PostInlineForm(forms.ModelForm):

    '''This form renders a model and adds a link to edit the nested inline
    model. This is useful for inline editing when the nested inline fields are
    not displayed.'''

    edit_link = forms.CharField(label='Edit', required=False)
    print_dates = forms.CharField(label='Post Person Dates', required=False)

    # verbose_name = 'Post'

    class Meta:
        exclude = ()
        fieldsets = []

    def __init__(self, *args, **kwargs):
        super(PostInlineForm, self).__init__(*args, **kwargs)

        # instance is always available, it just does or doesn't have pk.
        self.fields['edit_link'].widget = ModelLinkWidget(self.instance)
        self.fields['print_dates'].widget = PostAssertionDatesWidget(self.instance)


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
