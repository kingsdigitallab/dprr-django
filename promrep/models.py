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

        date_str = u'%s %s %s'.strip() % (self.date_type or '', abs(self.year), bc_ad)

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


class Gens(models.Model):

    class Meta:
        verbose_name_plural = "Gens"

    name = models.CharField(max_length=128, unique=True)
    extra_info = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.name


class Tribe(models.Model):
    abbrev = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=128)
    extra_info = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.abbrev

    class Meta:
        ordering = ['id', ]


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

NOTE_TYPES = (
    ('r', 'Reference (Body of text)'),
    ('e', 'Endnote (Broughton only)'),
)

class Note(TimeStampedModel):
    note_type = models.CharField(max_length=1, choices=NOTE_TYPES)

    # useful to store the bookmark number, for instance
    extra_info = models.CharField(max_length=128, blank=True)
    text = models.CharField(max_length=1024, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.text

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "text__icontains", )


@with_author
class AssertionNote(Note):
    pass

@with_author
class PersonNote(Note):
    pass


@with_author
class Person(TimeStampedModel):

    # TODO: should be string instead?
    praenomen = models.ForeignKey(Praenomen, blank=True, null=True)
    praenomen_certainty = models.BooleanField(verbose_name='Praenomen Certainty?', default=True)

    nomen = models.CharField(max_length=128, blank=True)
    cognomen = models.CharField(max_length=64, blank=True)

    other_names = models.CharField(max_length=128, blank=True)

    filiation = models.CharField(max_length=256, blank=True)
    gens = models.ForeignKey(Gens, blank=True, null=True)
    tribe = models.ForeignKey(Gens, blank=True, null=True)

    sex = models.ForeignKey(Sex, blank=True, null=True)

    real_number = models.CharField(max_length=32, blank=True, verbose_name='RE Number')
    real_number.help_text = "RE number"

    real_number_old = models.CharField(max_length=32, blank=True, verbose_name='RE (old)')
    real_number_old.help_text = "RE number before revising"

    real_attribute = models.CharField(max_length=128, blank=True, verbose_name='RE attribute')
    real_attribute.help_text = "Original RE entry (from source)"

    tribe = models.ForeignKey(Tribe, blank=True, null=True)

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
        r_id = ' '.join([self.real_number, self.real_attribute])

        return r_id.strip()

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

    def update_empty_fields(self, obj):
        """compares two objects, updating the empty fields from the first
        object with the values from the second object"""

        attrs = (
            'patrician_certainty',
            'patrician',
            'cognomen',
            'sex_id',
            'origin_id',
            'praenomen_certainty',
            'filiation',
            'gens_id',
            'other_names',
            'real_number_old',
            'real_attribute',
            'tribe_id',
            )

        return self._update_empty_fields(self, obj, attrs)

    def _update_empty_fields( self, obj1, obj2, keys ):
        (d1, d2) = (obj1.__dict__, obj2.__dict__)

        new_fields = []

        for k in keys:
            if d1[k] != d2[k]:
                # tests if the first object's field is empty
                if not d1[k] and d2[k]:
                    new_fields.append(k)
                    setattr(self, k, d2[k])

        self.save( update_fields = new_fields )

        return new_fields

    class Meta:
        ordering = ['id',]


# Broughton, Rupke, etc

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


class Assertion(TimeStampedModel):

    persons = models.ManyToManyField(Person, through='AssertionPerson')
    assertion_type = models.ForeignKey(AssertionType)

    # should these be combined into a single tree

    office = models.ForeignKey(Office, blank=True, null=True)
    relationship = models.ForeignKey(Relationship, blank=True, null=True)

    notes = models.ManyToManyField(AssertionNote)
    dates = models.ManyToManyField(AssertionDate)

    secondary_source = models.ForeignKey(SecondarySource)
    display_text = models.CharField(max_length=1024, blank=True)

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
        return dates

    get_dates.short_description = 'Dates'

    def __unicode__(self):
        name = self.assertion_type.name

        if self.office != None:
            name = name + " (" + self.office.name + ")"
        if self.relationship != None:
            name = name + " (" + self.relationship.name + ")"
            # should add the other person's name as well

        return name


class AssertionPerson(TimeStampedModel):
    person = models.ForeignKey(Person)
    assertion = models.ForeignKey(Assertion)

    role = models.ForeignKey(RoleType)
    original_text = models.CharField(max_length=1024, blank=True)

    certainty = models.BooleanField(verbose_name='Certainty?', default=True)

    notes = models.ManyToManyField(PersonNote)
    dates = models.ManyToManyField(AssertionPersonDate)

    def __unicode__(self):
        return str(self.person.__unicode__()) + ": " + str(self.assertion.__unicode__())
