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
class PostNote(Note):
    pass

@with_author
class PostAssertionNote(Note):

    def url_to_edit_note(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.__unicode__())

    def related_label(self):
        return u"[%s - %s] %s<br /><br />" % (self.get_note_type_display(), self.secondary_source.abbrev_name , self.text)


@with_author
class Person(TimeStampedModel):

    praenomen = models.ForeignKey(Praenomen, blank=True, null=True)
    praenomen_uncertain = models.BooleanField(verbose_name='Uncertain Praenomen', default=False)

    nomen = models.CharField(max_length=128, blank=True)
    nomen_uncertain = models.BooleanField(verbose_name='Uncertain Nomen', default=False)

    cognomen = models.CharField(max_length=64, blank=True)
    cognomen_uncertain = models.BooleanField(verbose_name='Uncertain Cognomen', default=False)

    other_names = models.CharField(max_length=128, blank=True)

    filiation = models.CharField(max_length=256, blank=True)
    filiation_uncertain = models.BooleanField(verbose_name='Uncertain Filiation', default=False)

    gens = models.ForeignKey(Gens, blank=True, null=True)
    gens_uncertain = models.BooleanField(verbose_name='Uncertain Gens', default=False)

    tribe = models.ForeignKey(Tribe, blank=True, null=True)
    tribe_uncertain = models.BooleanField(verbose_name='Uncertain Tribe', default=False)

    sex = models.ForeignKey(Sex, blank=True, null=True, default=1)

    re_number = models.CharField(max_length=32, blank=True, verbose_name='RE Number')
    re_number.help_text = "RE number"

    re_number_old = models.CharField(max_length=32, blank=True, verbose_name='RE (old)')
    re_number_old.help_text = "RE number before revising"

    origin = models.ForeignKey(Origin, blank=True, null=True)

    patrician = models.NullBooleanField(verbose_name='Patrician', default=None, null=True)
    patrician_uncertain = models.BooleanField(verbose_name='Uncertain Patrician', default=False)
    patrician_notes = models.TextField(blank=True)

    novus = models.NullBooleanField(default=None, null=True)
    novus_uncertain = models.NullBooleanField(default=False)
    novus_notes = models.TextField(blank=True)

    eques = models.NullBooleanField(default=None, null=True)
    eques_uncertain = models.BooleanField(default=False)
    eques_notes = models.TextField(blank=True)

    nobilis = models.NullBooleanField(default=None, null=True)
    nobilis_uncertain = models.BooleanField(default=False)
    nobilis_notes = models.TextField(blank=True)

    extra_info = models.TextField(blank=True)
    extra_info.help_text = "Extra info about the person."

    review_flag = models.BooleanField(verbose_name="Review needed", default=False)
    review_flag.help_text = "Person needs manual revision."

    def url_to_edit_person(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.module_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.__unicode__())

    url_to_edit_person.allow_tags = True
    url_to_edit_person.short_description = 'Person'

    def related_label(self):
        return self.url_to_edit_person()

    def __unicode__(self):
        name = ""

        if self.praenomen:
            name = name + ' ' + self.praenomen.abbrev

        if self.nomen:
            name = name + ' ' + self.nomen

        if self.re_number:
            name = name + ' ' + '(' + self.re_number + ')'

        if self.filiation:
            name = name + ' ' + self.filiation

        if self.tribe:
            name = name + ' ' + self.tribe.abbrev

        if self.cognomen:
            name = name + ' ' + self.cognomen

        if self.other_names:
            name = name + ' ' + self.other_names

        if self.patrician == True:
            name = name + ' ' + "Pat."

        return name.strip()


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

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = 'Office List'
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


@with_author
class Location(TimeStampedModel):
    LOCATION_PLACE = 0
    LOCATION_REGION = 1

    LOCATION_TYPE_CHOICES = (
        (LOCATION_PLACE, 'place'),
        (LOCATION_REGION, 'province'),
    )

    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)
    location_type = models.SmallIntegerField(choices=LOCATION_TYPE_CHOICES, default=LOCATION_PLACE)


    class Meta:
        verbose_name_plural = 'Place List'
        verbose_name = 'Places'

    def __unicode__(self):
        return self.name


@with_author
class Post(TimeStampedModel):
    persons = models.ManyToManyField(Person, through='PostAssertion')

    # should these be combined into a single tree
    office = models.ForeignKey(Office, blank=True, null=True)

    location = models.ForeignKey(Location, blank=True, null=True)
    notes = models.ManyToManyField(PostNote, related_name="posts", blank=True)

    display_text = models.CharField(max_length=1024, blank=True)

    # if we are uncertain about an assertion
    # ... eg. cases like Broughton's "Augur or Pontifex"
    uncertain = models.BooleanField(verbose_name='Uncertain', default=False)

    class Meta:
        ordering = ['id',]

    def get_persons(self):
        s = []
        for ap in self.postassertion_set.all():
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

        if len(self.dates.all()) > 0:
            name = name + " " + self.get_dates() + " "

        return name

    def related_label(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.module_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.__unicode__(), )



@with_author
class PostAssertion(TimeStampedModel):
    person = models.ForeignKey(Person)
    post = models.ForeignKey(Post)
    secondary_source = models.ForeignKey(SecondarySource)

    role = models.ForeignKey(RoleType, default=1)
    original_text = models.CharField(max_length=1024, blank=True)
    office_xref = models.CharField(max_length=1024, blank=True)

    uncertain = models.BooleanField(verbose_name='Uncertain', default=False)

    notes = models.ManyToManyField(PostAssertionNote, blank=True)

    # position field
    # used to set order in inline position
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['position', 'id']

    def __unicode__(self):
        name = str(self.person.__unicode__()) + ": " + str(self.post.__unicode__())
        name = name + " (" + self.secondary_source.abbrev_name + ")"
        return name

    def get_dates(self):
        dates = ' '.join([unicode(date) for date in self.dates.all()])
        return dates


class DateType(models.Model):

    name = models.CharField(max_length=32)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True, editable=False)

    class Meta:

        ordering = ['name']

    def __unicode__(self):
        return u'%s' % self.name


class Date(models.Model):

    date_type = models.ForeignKey(DateType, blank=True, null=True)

    start = models.IntegerField(min_value=-600, max_value=100, blank=True, null=False)
    start_uncertain = models.BooleanField(default=False)
    start_circa = models.BooleanField(default=False)

    end = models.IntegerField(min_value=-600, max_value=100, blank=True, null=False)
    end_uncertain = models.BooleanField(default=False)
    end_circa = models.BooleanField(default=False)

    start_alt = models.IntegerField(min_value=-600, max_value=100, blank=True, null=False)
    start_alt_uncertain = models.BooleanField(default=False)
    start_alt_circa = models.BooleanField(default=False)

    end_alt = models.IntegerField(min_value=-600, max_value=100, blank=True, null=False)
    end_alt_uncertain = models.BooleanField(default=False)
    end_alt_circa = models.BooleanField(default=False)

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

        date_str = u'%s %s%s %s'.strip() % (self.date_type or '', uncertain, self.year, bc_ad)

        if self.circa == True:
            date_str = "ca. " + date_str

        return date_str

    class Meta:
        abstract = True


@with_author
class PostDate(Date):
    post = models.ForeignKey(Post, related_name="dates", related_query_name="date", blank=True, null=True)

@with_author
class PostAssertionDate(Date):
    post_assertion = models.ForeignKey(PostAssertion, related_name="dates", related_query_name="date", blank=True, null=True)

@with_author
class PersonDate(Date):
    person = models.ForeignKey(Person, related_name="dates", related_query_name="date", blank=True, null=True)
