#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from model_utils.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.core.urlresolvers import reverse

from author.decorators import with_author

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

    year = IntegerRangeField(min_value=-500, max_value=500, blank=True, null=False)
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
    pass

@with_author
class AssertionPersonDate(Date):
    pass

@with_author
class PersonDate(Date):
    pass

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

    NOTE_TYPES = (
        (REFERENCE_NOTE, 'Reference'),
        (FOOTNOTE, 'Footnote'),
    )

    note_type = models.IntegerField(choices=NOTE_TYPES, default=REFERENCE_NOTE)

    # useful to store the bookmark number, for instance
    extra_info = models.TextField(max_length=1024, blank=True)
    text = models.TextField(max_length=2048, blank=True)

    class Meta:
        abstract = True
        ordering = ['id',]

    def __unicode__(self):
        return self.text.strip()

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "text__icontains", )


@with_author
class AssertionNote(Note):
    pass

@with_author
class AssertionPersonNote(Note):

    def related_label(self):
        return u"(%s) %s" % (self.get_note_type_display(), self.text)



@with_author
class Person(TimeStampedModel):

    praenomen = models.ForeignKey(Praenomen, blank=True, null=True)
    praenomen_certainty = models.BooleanField(verbose_name='Praenomen Certainty?', default=True)

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

    patrician = models.BooleanField(verbose_name='Patrician?', default=False)
    patrician_certainty = models.BooleanField(verbose_name='Patrician Certainty?', default=True)

    extra_info = models.CharField(max_length=1024, blank=True)
    extra_info.help_text = "Extra info about the person."

    review_flag = models.BooleanField(verbose_name="Review needed", default=False)
    review_flag.help_text = "Person needs manual revision."

    dates = models.ManyToManyField(PersonDate)

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "nomen__icontains", )

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
        url = reverse('admin:%s_%s_change' % (self._meta.app_label,
                      self._meta.module_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.__unicode__())

    url_to_edit_person.allow_tags = True
    url_to_edit_person.short_description = 'Person'

    def __unicode__(self):
        # TODO: add praenomen, Re number
        return self.get_name() + ' (' + self.real_id() + ')'

    def get_dates(self):
        dates = ' '.join([unicode(date) for date in self.dates.all()])
        return dates

    get_dates.short_description = 'Dates'

    class Meta:
        ordering = ['id',]


# Broughton, Rupke, etc
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
        return ("id__iexact", "name__icontains", "abbrev__icontains")


class PrimarySource(models.Model):

    name = models.CharField(max_length=256, unique=True)

    def __unicode__(self):
        return self.name


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
        return ("id__iexact", "name__icontains", )


@with_author
class Assertion(TimeStampedModel):

    persons = models.ManyToManyField(Person, through='AssertionPerson')
    assertion_type = models.ForeignKey(AssertionType)

    # should these be combined into a single tree

    office = models.ForeignKey(Office, blank=True, null=True)
    relationship = models.ForeignKey(Relationship, blank=True, null=True)

    notes = models.ManyToManyField(AssertionNote, related_name="assertions")
    dates = models.ManyToManyField(AssertionDate, related_name="assertions")

    secondary_source = models.ForeignKey(SecondarySource)
    display_text = models.CharField(max_length=1024, blank=True)

    # if we are uncertain about an assertion
    # ... eg. cases like Broughton's "Augur or Pontifex"
    certainty = models.BooleanField(verbose_name='Certainty?', default=True)

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

        name = name + " (" + self.secondary_source.abbrev_name + ")"

        return name


@with_author
class AssertionPerson(TimeStampedModel):
    person = models.ForeignKey(Person)
    assertion = models.ForeignKey(Assertion)

    role = models.ForeignKey(RoleType)
    original_text = models.CharField(max_length=1024, blank=True)
    office_xref = models.CharField(max_length=1024, blank=True)

    certainty = models.BooleanField(verbose_name='Certainty?', default=True)

    notes = models.ManyToManyField(AssertionPersonNote)
    dates = models.ManyToManyField(AssertionPersonDate)

    # position field
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['position', 'id']


    def __unicode__(self):
        return str(self.person.__unicode__()) + ": " + str(self.assertion.__unicode__())


class AssertionNoteThrough(Assertion.notes.through):
    class Meta:
        proxy = True

    def __unicode__(self):
        snippet = (self.assertionnote.text[:120] + ' ...') if len(self.assertionnote.text) > 120 else self.assertionnote.text

        return '- "%s"' %(snippet.strip())