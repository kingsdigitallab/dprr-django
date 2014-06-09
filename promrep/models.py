#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
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

    tribe = models.CharField(max_length=128, blank=True)

    is_patrician = models.BooleanField(blank=True, verbose_name='Patrician')
    patrician_certainty = models.ForeignKey(Certainty,
            related_name='person_patrician_certainty', null=True,
            blank=True)

    is_noble = models.BooleanField(blank=True, verbose_name='Noble')
    noble_certainty = models.ForeignKey(Certainty,
            related_name='person_noble_certainty', null=True,
            blank=True)

    is_novus_homo = models.BooleanField(default=False, blank=True,
            verbose_name='Novus Homo')
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

        name_parts = [self.nomen, self.cognomen_first,
                      self.cognomen_other]

        if self.praenomen:
            name = self.praenomen.abbrev + ' '.join(name_parts)
        else:
            name = ' '.join(name_parts)

        return name

    def url_to_edit_person(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label,
                      self._meta.module_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.__unicode__())

    url_to_edit_person.allow_tags = True
    url_to_edit_person.short_description = 'Person'

    def __unicode__(self):

        # TODO: add praenomen, Re number

        return self.get_name() + ' (' + self.real_id() + ')'


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


class AssertionType(models.Model):

    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Assertion(TimeStampedModel):

    persons = models.ManyToManyField(Person, through='AssertionPerson')
    assertion_type = models.ForeignKey(AssertionType)
    office = models.ForeignKey(Office)

    secondary_source = models.ForeignKey(SecondarySource)

    display_text = models.CharField(max_length=1024, blank=True)
    date_year = models.CharField(max_length=64, blank=True)

    notes = models.CharField(max_length=1024, blank=True)

    def get_persons(self):
        return '\n'.join([str(a) for a in self.persons.all()])

    def __unicode__(self):
        type = self.assertion_type.name
        office = self.office.name

        if office != None:
            office = self.office.name

        return type + " (" + office + ")"


class AssertionPerson(TimeStampedModel):

    person = models.ForeignKey(Person)
    assertion = models.ForeignKey(Assertion)

    role = models.ForeignKey(RoleType)
    original_text = models.CharField(max_length=1024, blank=True)


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

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    date_type = models.ForeignKey(DateType, blank=True, null=True)
    interval = \
        models.SmallIntegerField(choices=settings.DATE_INTERVAL_CHOICES)
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
        return u'%s %s-%s-%s'.strip() % (self.date_type or '',
                self.year, self.month, self.day)
