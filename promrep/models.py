#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from model_utils.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.core.urlresolvers import reverse


class IntegerRangeField(models.IntegerField):

    def __init__(
        self,
        verbose_name=None,
        name=None,
        min_value=None,
        max_value=None,
        **kwargs
        ):

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
    DATE_INTERVAL_CHOICES = ((DATE_SINGLE, 'single'), (DATE_MIN, 'min'
                             ), (DATE_MAX, 'max'))

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    date_type = models.ForeignKey(DateType, blank=True, null=True)
    interval = \
        models.SmallIntegerField(choices=DATE_INTERVAL_CHOICES)
    year = IntegerRangeField(min_value=-500, max_value=500, blank=True,
                             null=True)
    year_uncertain = models.BooleanField(verbose_name='uncertain')
    month = IntegerRangeField(min_value=1, max_value=12, blank=True,
                              null=True)
    month_uncertain = models.BooleanField(verbose_name='uncertain')
    day = IntegerRangeField(min_value=1, max_value=31, blank=True,
                            null=True)
    day_uncertain = models.BooleanField(verbose_name='uncertain')
    circa = models.BooleanField()
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True,
                                    editable=False)

    def __unicode__(self):

        if self.year < 0:
            bc_ad = "BC"
        else:
            bc_ad = "AD"

        date_str = u'%s %s %s'.strip() % (self.date_type or '', abs(self.year), bc_ad)

        return date_str


class Praenomen(models.Model):

    abbrev = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:

        verbose_name_plural = 'Praenomina'
        ordering = ['name']


class Sex(models.Model):

    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.name


class RoleType(TimeStampedModel):

    name = models.CharField(max_length=128, unique=True)

    description = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.name


class Certainty(models.Model):

    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return self.name


class Person(TimeStampedModel):

    original_text = models.CharField(max_length=256, blank=True)

    praenomen = models.ForeignKey(Praenomen, blank=True, null=True)
    nomen = models.CharField(max_length=128, blank=True)

    cognomen_first = models.CharField(max_length=64, blank=True)
    cognomen_other = models.CharField(max_length=128, blank=True)

    sex = models.ForeignKey(Sex, blank=True, null=True)

    dates = generic.GenericRelation(Date)

    tribe = models.CharField(max_length=128, blank=True)

    is_patrician = models.BooleanField(blank=True,
            verbose_name='Patrician')
    patrician_certainty = models.ForeignKey(Certainty,
            related_name='person_patrician_certainty', null=True,
            blank=True)

    consular_ancestor = models.BooleanField(blank=True,
            verbose_name='Consular Ancestor?')
    consular_ancestor_certainty = models.ForeignKey(Certainty,
            related_name='person_noble_certainty', null=True,
            blank=True)

    novus_homo = models.BooleanField(default=False, blank=True,
            verbose_name='Novus Homo?')
    novus_homo_certainty = models.ForeignKey(Certainty,
            related_name='person_novus_homo_certainty', null=True,
            blank=True)

    notes = models.CharField(max_length=1024, blank=True)
    filiation = models.CharField(max_length=256, blank=True)

    real_number = models.CharField(max_length=32, blank=True,
                                   verbose_name='RE Number')
    real_number_old = models.CharField(max_length=32, blank=True,
            verbose_name='RE Number (Starred)')

    real_attribute = models.CharField(max_length=128, blank=True)

    def cognomen(self):
        return self.cognomen_first + self.cognomen_other

    def real_id(self):
        r_id = ' '.join([self.real_number, self.real_attribute])

        return r_id.strip()

    def get_name(self):

        name_parts = [self.nomen, self.filiation, self.cognomen_first,
                      self.cognomen_other]

        if self.praenomen:
            name = self.praenomen.abbrev + ' '
        else:
            name = ''

        return name + ' '.join(name_parts)

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

    def compare(self, obj):
        excluded_keys = (
            'created',
            '_state',
            'modified',
            '_praenomen_cache',
            '_sex_cache',
            'id',
            )
        return self._compare(self, obj, excluded_keys)

    def _compare(
        self,
        obj1,
        obj2,
        excluded_keys,
        ):
        (d1, d2) = (obj1.__dict__, obj2.__dict__)
        (old, new) = ({}, {})
        for (k, v) in d1.items():
            if k in excluded_keys:
                continue
            try:
                if v != d2[k]:
                    old.update({k: v})
                    new.update({k: d2[k]})
            except KeyError:
                old.update({k: v})

        return (old, new)


# Broughton, Rupke, etc

class SecondarySource(TimeStampedModel):

    name = models.CharField(max_length=256, unique=True)

    abbrev_name = models.CharField(max_length=256, unique=True,
                                   blank=True)
    biblio = models.CharField(max_length=512, unique=True, blank=True)

    def __unicode__(self):
        return self.abbrev_name


#

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


class Relationship(TimeStampedModel):

    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.name


class AssertionType(models.Model):

    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Assertion(TimeStampedModel):

    persons = models.ManyToManyField(Person, through='AssertionPerson')
    assertion_type = models.ForeignKey(AssertionType)

    # should these be combined into a single tree

    office = models.ForeignKey(Office, blank=True, null=True)
    relationship = models.ForeignKey(Relationship, blank=True,
            null=True)

    dates = generic.GenericRelation(Date)

    secondary_source = models.ForeignKey(SecondarySource)

    display_text = models.CharField(max_length=1024, blank=True)

    notes = models.CharField(max_length=1024, blank=True)

    def get_persons(self):
        return '\n'.join([str(a) for a in self.persons.all()])
    get_persons.short_description = "Persons"

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

    def __unicode__(self):
        return str(self.person.__unicode__()) + ": " + str(self.assertion.__unicode__())
