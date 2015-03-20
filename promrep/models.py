#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from model_utils.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.core import urlresolvers
from django.core.urlresolvers import reverse

from author.decorators import with_author

@with_author
class SecondarySource(TimeStampedModel):

    name = models.CharField(max_length=256, unique=True)

    abbrev_name = models.CharField(max_length=256, unique=True,
                                   blank=True)
    biblio = models.CharField(max_length=512, unique=True, blank=True)

    def __unicode__(self):
        return self.abbrev_name

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name", "abbrev")


class PrimarySource(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __unicode__(self):
        return self.name

@with_author
class Praenomen(models.Model):

    abbrev = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Praenomina'
        ordering = ['name']


class Sex(models.Model):

    name = models.CharField(max_length=32, unique=True)

    def __unicode__(self):
        return self.name

@with_author
class Gens(models.Model):

    class Meta:
        verbose_name_plural = "Gens"

    name = models.CharField(max_length=128, unique=True)
    extra_info = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.name

@with_author
class Tribe(models.Model):
    abbrev = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=128)
    extra_info = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.abbrev

    class Meta:
        ordering = ['id', ]

@with_author
class Origin(models.Model):

    name = models.CharField(max_length=128, unique=True)
    extra_info = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.name


class RoleType(TimeStampedModel):

    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.name

class Note(TimeStampedModel):
    REFERENCE_NOTE = 0
    FOOTNOTE = 1
    OFFICE_NOTE = 2
    OFFICE_FOOTNOTE = 3

    NOTE_TYPES = (
        (REFERENCE_NOTE, 'Reference'),
        (FOOTNOTE, 'Footnote'),
        (OFFICE_NOTE, 'Reference (Office)'),
        (OFFICE_FOOTNOTE, 'Footnote (Office)')
    )

    note_type = models.IntegerField(choices=NOTE_TYPES, default=REFERENCE_NOTE)
    secondary_source = models.ForeignKey(SecondarySource)

    # useful to store the bookmark number, for instance
    text = models.TextField(blank=True)
    extra_info = models.TextField(max_length=1024, blank=True)

    class Meta:
        abstract = True
        ordering = ['id',]

    def __unicode__(self):
        return self.text.strip()

@with_author
class AssertionNote(Note):
    pass

@with_author
class AssertionPersonNote(Note):

    def url_to_edit_note(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.module_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.__unicode__())

    def related_label(self):

        return u"[%s - %s] %s<br /><br />" % (self.get_note_type_display(), self.secondary_source.abbrev_name , self.text)



@with_author
class Person(TimeStampedModel):

    praenomen = models.ForeignKey(Praenomen, blank=True, null=True)
    praenomen_uncertain = models.BooleanField(verbose_name='Uncertain Praenomen', default=False)

    nomen = models.CharField(max_length=128, blank=True)
    cognomen = models.CharField(max_length=64, blank=True)

    other_names = models.CharField(max_length=128, blank=True)

    filiation = models.CharField(max_length=256, blank=True)
    gens = models.ForeignKey(Gens, blank=True, null=True)
    tribe = models.ForeignKey(Tribe, blank=True, null=True)

    sex = models.ForeignKey(Sex, blank=True, null=True, default=1)

    real_number = models.CharField(max_length=32, blank=True, verbose_name='RE Number')
    real_number.help_text = "RE number"

    real_number_old = models.CharField(max_length=32, blank=True, verbose_name='RE (old)')
    real_number_old.help_text = "RE number before revising"

    origin = models.ForeignKey(Origin, blank=True, null=True)

    patrician = models.BooleanField(verbose_name='Patrician', default=False)
    patrician_uncertain = models.BooleanField(verbose_name='Uncertain Patrician', default=False)

    extra_info = models.CharField(max_length=1024, blank=True)
    extra_info.help_text = "Extra info about the person."

    review_flag = models.BooleanField(verbose_name="Review needed", default=False)
    review_flag.help_text = "Person needs manual revision."

    def real_id(self):
        return self.real_number

    def get_name(self):

        tribe_abbrev = ''
        if self.tribe:
            tribe_abbrev = self.tribe.abbrev

        prae_abbrev = ''
        if self.praenomen:
            prae_abbrev = self.praenomen.abbrev

        name_parts = [prae_abbrev, self.nomen, self.filiation, tribe_abbrev, self.cognomen, self.other_names]

        # remove empty strings and concatenate
        return ' '.join(filter(None, name_parts))

    def url_to_edit_person(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.module_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.__unicode__())

    url_to_edit_person.allow_tags = True
    url_to_edit_person.short_description = 'Person'

    def related_label(self):
        return self.url_to_edit_person()

    def __unicode__(self):

        # TODO: add praenomen, Re number
        if self.real_id():
            return self.get_name() + ' (' + self.real_id() + ')'
        else:
            return self.get_name()

#    def get_dates(self):
#        dates = ' '.join([unicode(date) for date in self.dates.all()])
#        return dates

#    get_dates.short_description = 'Dates'

    class Meta:
        ordering = ['id',]


@with_author
class Office(MPTTModel, TimeStampedModel):

    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)

    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')

    class Meta:
        verbose_name_plural = 'Offices'
        verbose_name = 'Office List'
        ordering = ['tree_id', 'lft', 'name']

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)

@with_author
class Relationship(TimeStampedModel):

    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.name


class AssertionType(models.Model):

    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name", )


@with_author
class Assertion(TimeStampedModel):

    persons = models.ManyToManyField(Person, through='AssertionPerson')
    assertion_type = models.ForeignKey(AssertionType)

    # should these be combined into a single tree

    office = models.ForeignKey(Office, blank=True, null=True)
    relationship = models.ForeignKey(Relationship, blank=True, null=True)

    notes = models.ManyToManyField(AssertionNote, related_name="assertions")

    display_text = models.CharField(max_length=1024, blank=True)

    # if we are uncertain about an assertion
    # ... eg. cases like Broughton's "Augur or Pontifex"
    uncertain = models.BooleanField(verbose_name='Uncertain', default=False)

    class Meta:
        ordering = ['id',]

    def get_persons(self):
        s = []
        for ap in self.assertionperson_set.all():
            s.append(ap.person.__unicode__() + ' [' + ap.role.name + ']')

        return '; '.join(s)

    get_persons.short_description = "Persons"

    def get_dates(self):
        dates = ' '.join([unicode(date) for date in self.dates.all()])
        return dates.strip()

    get_dates.short_description = 'Dates'

    def __unicode__(self):
        name = ""

        if self.office != None:
            name = self.office.name
        if self.relationship != None:
            name = self.relationship.name
            # should add the other person's name as well

        if len(self.dates.all()) > 0:
            name = name + " " + self.get_dates() + " "

        return name

    def related_label(self):
        change_url = urlresolvers.reverse('admin:promrep_assertion_change', args=(self.id,))

        return u'<a href="%s">%s</a>' % (change_url, self.__unicode__(), )



@with_author
class AssertionPerson(TimeStampedModel):
    person = models.ForeignKey(Person)
    assertion = models.ForeignKey(Assertion)
    secondary_source = models.ForeignKey(SecondarySource)

    role = models.ForeignKey(RoleType)
    original_text = models.CharField(max_length=1024, blank=True)
    office_xref = models.CharField(max_length=1024, blank=True)

    uncertain = models.BooleanField(verbose_name='Uncertain', default=False)

    notes = models.ManyToManyField(AssertionPersonNote)

    # position field
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['position', 'id']

    def __unicode__(self):
        name = str(self.person.__unicode__()) + ": " + str(self.assertion.__unicode__())
        name = name + " (" + self.secondary_source.abbrev_name + ")"
        return name

    def get_dates(self):
        dates = ' '.join([unicode(date) for date in self.dates.all()])
        return dates


class IntegerRangeField(models.IntegerField):
    def __init__(self,
                 verbose_name=None,
                 name=None,
                 min_value=None,
                 max_value=None,
                 **kwargs):

        (self.min_value, self.max_value) = (min_value, max_value)
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value,
                    'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^promrep\.models\.IntegerRangeField"])

class DateType(models.Model):

    name = models.CharField(max_length=32)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True,
                                    editable=False)

    class Meta:

        ordering = ['name']

    def __unicode__(self):
        return u'%s' % self.name


class Date(models.Model):

    # Promrep settings

    DATE_SINGLE = 0
    DATE_MIN = 1
    DATE_MAX = 2
    DATE_INTERVAL_CHOICES = ((DATE_SINGLE, 'single'), (DATE_MIN, 'min'), (DATE_MAX, 'max'))

    date_type = models.ForeignKey(DateType, blank=True, null=True)
    interval = models.SmallIntegerField(choices=DATE_INTERVAL_CHOICES, default=DATE_SINGLE)

    year = IntegerRangeField(min_value=-600, max_value=100, blank=True, null=False)
    year_uncertain = models.BooleanField(verbose_name='uncertain', default=False)

    circa = models.BooleanField(default=False)
    extra_info = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True, editable=False)

    def __unicode__(self):

        if self.year < 0:
            bc_ad = "BC"
        else:
            bc_ad = "AD"

        if self.year_uncertain:
            uncertain = "?"
        else:
            uncertain = ""

        date_str = u'%s %s%s %s'.strip() % (self.date_type or '', abs(self.year), uncertain, bc_ad)

        if self.circa == True:
            date_str = "ca. " + date_str

        return date_str

    class Meta:
        abstract = True


@with_author
class AssertionDate(Date):
    assertion = models.ForeignKey(Assertion, related_name="dates", related_query_name="date", blank=True, null=True)

@with_author
class AssertionPersonDate(Date):
    assertion_person = models.ForeignKey(AssertionPerson, related_name="dates", related_query_name="date", blank=True, null=True)

@with_author
class PersonDate(Date):
    person = models.ForeignKey(Person, related_name="dates", related_query_name="date", blank=True, null=True)
