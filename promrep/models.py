#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from model_utils.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from django.core import urlresolvers
from django.core.urlresolvers import reverse

from author.decorators import with_author


def date_to_string(date_int, date_uncertain, date_suffix=True):
    date_str = ""
    suffix = " B.C."

    if date_uncertain:
        date_str = "?"

    if date_int:
        if date_int > 0:
            date_str = date_str + str(date_int)
            suffix = " A.D."
        else:
            date_str = date_str + str(abs(date_int))

        if date_suffix:
            date_str = date_str + suffix
    else:
        date_str = "<i>(no date info)</i>"

    return date_str


@with_author
class SecondarySource(TimeStampedModel):

    name = models.CharField(max_length=256, unique=True)
    abbrev_name = models.CharField(max_length=256, unique=True, blank=True)
    biblio = models.CharField(max_length=512, unique=True, blank=True)

    def __unicode__(self):
        return self.abbrev_name

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name", "abbrev")


class PrimarySource(models.Model):

    name = models.CharField(max_length=256, unique=True)
    abbrev_name = models.CharField(max_length=256, unique=True, blank=True)
    biblio = models.CharField(max_length=512, unique=True, blank=True)

    def __unicode__(self):
        return self.abbrev_name


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


class NoteType(TimeStampedModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.name


@with_author
class PrimarySourceReference(TimeStampedModel):
    # this is the connecting model between
    #   Note and PrimarySource

    limit = models.Q(app_label='promrep', model='PersonNote') | \
        models.Q(app_label='promrep', model='PostAssertionNote') | \
        models.Q(app_label='promrep', model='RelationshipAssertionReference')

    content_type = models.ForeignKey(
        ContentType,
        verbose_name='primary source reference',
        limit_choices_to=limit,
        null=True,
        blank=True,
    )

    object_id = models.PositiveIntegerField(
        verbose_name='related object',
        null=True,
    )

    content_object = GenericForeignKey('content_type', 'object_id')

    primary_source = models.ForeignKey(PrimarySource, null=True)
    text = models.TextField(blank=True)

    def __unicode__(self):
        return self.text


class Note(TimeStampedModel):
    # TODO: rename to SecondarySourceReference?
    note_type = models.ForeignKey(NoteType, default=1, )
    secondary_source = models.ForeignKey(SecondarySource)

    text = models.TextField(blank=True)

    # useful to store the bookmark number, for instance
    extra_info = models.TextField(max_length=1024, blank=True)

    class Meta:
        abstract = True
        ordering = ['id', ]

    def __unicode__(self):
        return self.text.strip()


def create_primary_source_reference(sender, **kwargs):
    if 'created' in kwargs:
        if kwargs['created']:
            instance = kwargs['instance']
            ctype = ContentType.objects.get_for_model(instance)
            primary_source_reference = PrimarySourceReference.objects.get_or_create(content_type=ctype,
                                                                                    object_id=instance.id,
                                                                                    pub_date=instance.pub_date)


@with_author
class RelationshipAssertionReference(Note):
    """This is a SecondarySourceNote/Reference

    """

    primary_source_references = GenericRelation(PrimarySourceReference,
                                                related_query_name='relationship_assertion_references')

    def print_primary_source_refs(self):
        return ', '.join([pref.__unicode__() for pref in self.primary_source_references.all()])

    def url_to_edit_note(self):
        url = reverse('admin:%s_%s_change' % (
            self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.__unicode__())

    def related_label(self):
        return u"[%s] %s (%s)<br /><br />" % (self.secondary_source.abbrev_name, self.text, self.print_primary_source_refs())

    def __unicode__(self):
        return u"%s, %s (%s)" % (self.secondary_source.abbrev_name, self.text, self.print_primary_source_refs())


@with_author
class PostAssertionNote(Note):

    def url_to_edit_note(self):
        url = reverse('admin:%s_%s_change' % (
            self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.__unicode__())

    def related_label(self):
        return u"[%s - %s] %s<br /><br />" % (self.note_type, self.secondary_source.abbrev_name, self.text)


@with_author
class PersonNote(Note):

    def url_to_edit_note(self):
        url = reverse('admin:%s_%s_change' % (
            self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.__unicode__())

    def related_label(self):
        return u"[%s - %s] %s<br /><br />" % (self.note_type, self.secondary_source.abbrev_name, self.text)


@with_author
class Person(TimeStampedModel):

    praenomen = models.ForeignKey(Praenomen, blank=True, null=True)
    praenomen_uncertain = models.BooleanField(
        verbose_name='Uncertain Praenomen', default=False)
    alt_praenomen = models.ForeignKey(Praenomen, blank=True, null=True,
                                      related_name='person_alt_praenomen_set',
                                      verbose_name='Alternative Praenomen')

    nomen = models.CharField(max_length=128, blank=True)
    nomen_uncertain = models.BooleanField(
        verbose_name='Uncertain Nomen', default=False)

    cognomen = models.CharField(max_length=64, blank=True)
    cognomen_uncertain = models.BooleanField(
        verbose_name='Uncertain Cognomen', default=False)

    other_names = models.CharField(max_length=128, blank=True)
    other_names_uncertain = models.BooleanField(
        verbose_name='Uncertain Other Names', default=False)

    filiation = models.CharField(max_length=256, blank=True)
    filiation_uncertain = models.BooleanField(
        verbose_name='Uncertain Filiation', default=False)

    gens = models.ForeignKey(Gens, blank=True, null=True)
    gens_uncertain = models.BooleanField(
        verbose_name='Uncertain Gens', default=False)

    tribe = models.ForeignKey(Tribe, blank=True, null=True)
    tribe_uncertain = models.BooleanField(
        verbose_name='Uncertain Tribe', default=False)

    sex = models.ForeignKey(Sex, blank=True, null=True, default=1)

    re_number = models.CharField(
        max_length=32, blank=True, verbose_name='RE Number')
    re_number.help_text = "RE number"

    re_number_old = models.CharField(
        max_length=32, blank=True, verbose_name='RE (old)')
    re_number_old.help_text = "RE number before revising"

    origin = models.ForeignKey(Origin, blank=True, null=True)

    patrician = models.NullBooleanField(
        verbose_name='Patrician', default=None, null=True)
    patrician_uncertain = models.BooleanField(
        verbose_name='Uncertain Patrician', default=False)
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

    notes = models.ManyToManyField(PersonNote, blank=True)

    # dates
    date_display_text = models.CharField(
        max_length=1024, blank=True, null=True)
    date_source_text = models.CharField(max_length=1024, blank=True, null=True)
    era_from = models.IntegerField(blank=True, null=True)
    era_to = models.IntegerField(blank=True, null=True)

    review_flag = models.BooleanField(
        verbose_name="Review needed", default=False)
    review_flag.help_text = "Person needs manual revision."

    review_notes = models.TextField(blank=True)

    def url_to_edit_person(self):
        url = reverse('admin:%s_%s_change' % (
            self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.__unicode__())

    url_to_edit_person.allow_tags = True
    url_to_edit_person.short_description = 'Person'

    def related_label(self):
        return self.url_to_edit_person()

    def __unicode__(self):
        name = ""

        # only show praenomen for men
        if self.sex.name == "Male":

            if self.praenomen:
                name = self.praenomen.abbrev

                if self.alt_praenomen:
                    name = name + " (or " + self.alt_praenomen.abbrev + ")"
                elif self.praenomen_uncertain:
                    name = name + "?"

        if self.nomen:
            name = name + ' ' + self.nomen

        if self.re_number:
            name = name + ' ' + '(' + self.re_number + ')'

        if self.filiation:
            if self.filiation not in ['- f. - n.', '- f.', '- n.']:
                name = name + ' ' + self.filiation

        if self.tribe:
            name = name + ' ' + self.tribe.abbrev

        if self.cognomen:
            name = name + ' ' + self.cognomen

        if self.other_names:
            name = name + ' ' + self.other_names

        return name.strip()


#    def get_dates(self):
#        dates = ' '.join([unicode(date) for date in self.dates.all()])
#        return dates

#    get_dates.short_description = 'Dates'

    class Meta:
        ordering = ['id', ]


@with_author
class DateType(TimeStampedModel):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % self.name


# @with_author
# class DateInformation(TimeStampedModel):
#     date_secondary_source = models.ForeignKey(
#         SecondarySource, blank=True, null=True)

#     date_first = models.IntegerField(blank=True, null=True)
#     date_first_type = models.ForeignKey(
#         DateType, blank=True, null=True, related_name='person_first')

#     date_last = models.IntegerField(blank=True, null=True)
#     date_last_type = models.ForeignKey(
#         DateType, blank=True, null=True, related_name='person_last')

#     class Meta:
#         verbose_name = 'Date'


@with_author
class Office(MPTTModel, TimeStampedModel):

    name = models.CharField(max_length=256, unique=True)
    abbrev_name = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=1024, blank=True)

    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = 'Office'
        verbose_name = 'Office'
        ordering = ['tree_id', 'lft', 'name']

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains",)


@with_author
class RelationshipType(TimeStampedModel):

    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.name


@with_author
class Province(TimeStampedModel):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)

    class Meta:
        verbose_name_plural = 'Provinces'
        verbose_name = 'Province'

    def __unicode__(self):
        return self.name


@with_author
class Group(TimeStampedModel):
    persons = models.ManyToManyField(Person, through='PostAssertion')
    display_text = models.CharField(max_length=1024, blank=True)

    notes = models.TextField(blank=True)

    # date information
    date_year = models.IntegerField(blank=True, null=True)
    date_info = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        ordering = ['id', ]

    def get_persons(self):
        s = []
        for ap in self.postassertion_set.all():
            s.append(ap.person.__unicode__() + ' [' + ap.role.name + ']')

        return '; '.join(s)

    get_persons.short_description = "Persons"

    def print_date(self):
        if self.date_year:
            if self.date_year < 0:
                return str(abs(self.date_year)) + " B.C."
            else:
                return str(self.date_year) + " A.D."
        else:
            return ""

    def __unicode__(self):
        members = str(self.persons.count())
        office_list = Office.objects.filter(
            postassertion__group=self).distinct().values_list('name', flat=True)

        offices = "; ".join(office_list)

        return "Group: {0} members; Office: {1} ({2})".format(members, offices, self.date_info)

    def related_label(self):
        url = reverse('admin:%s_%s_change' % (
            self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.__unicode__(), )


@with_author
class PostAssertion(TimeStampedModel):
    person = models.ForeignKey(Person, related_name='post_assertions')
    office = models.ForeignKey(Office)

    group = models.ForeignKey(Group, blank=True, null=True)
    secondary_source = models.ForeignKey(SecondarySource)

    provinces = models.ManyToManyField(
        Province, blank=True, through='PostAssertionProvince')
    province_original = models.CharField(max_length=512, blank=True)
    province_original_expanded = models.CharField(max_length=512, blank=True)

    role = models.ForeignKey(RoleType, default=1)
    original_text = models.CharField(max_length=1024, blank=True)
    office_xref = models.CharField(max_length=1024, blank=True)

    uncertain = models.BooleanField(verbose_name='Uncertain', default=False)

    notes = models.ManyToManyField(PostAssertionNote, blank=True)

    # position field
    # used to set order in inline position
    position = models.PositiveSmallIntegerField(default=0)

    # date information
    date_start = models.IntegerField(blank=True, null=True)
    date_start_uncertain = models.BooleanField(default=False)

    date_end = models.IntegerField(blank=True, null=True)
    date_end_uncertain = models.BooleanField(default=False)

    date_display_text = models.CharField(
        max_length=1024, blank=True, null=True)
    date_source_text = models.CharField(max_length=1024, blank=True, null=True)
    date_secondary_source = models.ForeignKey(
        SecondarySource, blank=True, null=True, related_name='postassertion_date_secondary_source')

    review_flag = models.BooleanField(
        verbose_name="Review needed", default=False)
    review_flag.help_text = "Manual revision needed."

    def print_provinces(self):
        provinces = []

        if self.id:
            for prov in self.postassertionprovince_set.all():
                name = str(prov.province)
                if prov.uncertain:
                    name = name + "?"

                provinces.append(name)

        return ", ".join(provinces)

    print_provinces.allow_tags = True
    print_provinces.short_description = 'Provinces'

    class Meta:
        ordering = ['-date_end', '-date_start', ]

    def __unicode__(self):

        off = "No office"
        if self.office:
            off = self.office.__unicode__()

        name = str(self.person.__unicode__()) + \
            ": " + off + " " + self.print_date()
        name = name + " (" + self.secondary_source.abbrev_name + ")"
        return name

    def print_date(self):
        date_str = ""

        if self.date_display_text:
            date_str = self.date_display_text
        elif self.date_start == self.date_end and self.date_start_uncertain == self.date_end_uncertain:
            date_str = date_to_string(
                self.date_start, self.date_start_uncertain)
        else:
            if self.date_start:
                date_str = date_to_string(
                    self.date_start, self.date_start_uncertain, False)
            else:
                date_str = "?"

            date_str = date_str + " - "

            if self.date_end:
                date_str = date_str + \
                    date_to_string(self.date_end, self.date_end_uncertain)
            else:
                date_str = date_str + "?"

        return date_str.strip()


@with_author
class PostAssertionProvince(models.Model):
    post_assertion = models.ForeignKey(PostAssertion)
    province = models.ForeignKey(Province)
    uncertain = models.BooleanField(verbose_name='Uncertain', default=False)
    note = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        un = ""
        if self.uncertain:
            un = "?"

        return self.province.name + " " + un


@with_author
class RelationshipAssertion(TimeStampedModel):
    person = models.ForeignKey(
        Person, related_name="relationships_as_subject")
    relationship = models.ForeignKey(RelationshipType)
    related_person = models.ForeignKey(
        Person, related_name="relationships_as_object")

    # relationship number indicates if it's the third wife of
    relationship_number = models.PositiveSmallIntegerField(
        null=True, blank=True)
    # when referring to the third wife of it's also useful to link to the other
    # relationship - in this case the previous
    related_relationship = models.ForeignKey("self", null=True, blank=True,
                                             related_name="next")

    # when two different sources write about the two sides of the relationship
    # this field indicates that one is the inverse of the other
    inverse_relationship = models.ForeignKey("self", null=True, blank=True)

    uncertain = models.BooleanField(verbose_name='Uncertain', default=False)

    original_text = models.CharField(max_length=1024, blank=True)

    # TODO: should this be removed - and use the Note instead?
    secondary_source = models.ForeignKey(SecondarySource)

    # TODO: normalise - same as PostAssertionNotes
    references = models.ManyToManyField(
        RelationshipAssertionReference, blank=True)

    extra_info = models.TextField(blank=True)
    extra_info.help_text = "Extra info about the relationship"

    review_flag = models.BooleanField(
        verbose_name="Review needed", default=False)

    def __unicode__(self):
        return "{} is {} {}".format(self.person, self.relationship, self.related_person)

    class Meta:
        ordering = ['relationship_number', 'id']
