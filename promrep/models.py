#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from author.decorators import with_author
from django.conf import settings as s
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.html import mark_safe
from model_utils.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey


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
        date_str = "date uncertain"

    return date_str


@with_author
class SecondarySource(TimeStampedModel):
    name = models.CharField(max_length=256, unique=True)
    abbrev_name = models.CharField(max_length=256, unique=True, blank=True)
    biblio = models.CharField(max_length=512, unique=True, blank=True)

    def __unicode__(self):
        return self.abbrev_name

    def __str__(self):
        return self.__unicode__()

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name", "abbrev_name")


class PrimarySource(models.Model):
    name = models.CharField(max_length=256, unique=True)
    abbrev_name = models.CharField(max_length=256, unique=True, blank=True)
    biblio = models.CharField(max_length=512, unique=True, blank=True)

    def __unicode__(self):
        return self.abbrev_name

    def __str__(self):
        return self.__unicode__()


@with_author
class Praenomen(models.Model):
    abbrev = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = "Praenomina"
        ordering = ["name"]

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    @property
    def alternate_name(self):
        if self.has_alternate_name():
            return "C" + self.name[1:]

        return None

    def has_alternate_name(self):
        if not self.name:
            return False

        return self.name[0].upper() == "G"


class Sex(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


@with_author
class Gens(models.Model):
    class Meta:
        verbose_name_plural = "Gens"

    name = models.CharField(max_length=128, unique=True)
    extra_info = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


@with_author
class Tribe(models.Model):
    abbrev = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=128)
    extra_info = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.abbrev

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = [
            "id",
        ]


class NoteType(TimeStampedModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


@with_author
class PrimarySourceReference(TimeStampedModel):
    # this is the connecting model between
    #   Note and PrimarySource

    limit = (
        models.Q(app_label="promrep", model="PersonNote")
        | models.Q(app_label="promrep", model="PostAssertionNote")
        | models.Q(app_label="promrep", model="RelationshipAssertionReference")
    )

    content_type = models.ForeignKey(
        ContentType,
        verbose_name="primary source reference",
        limit_choices_to=limit,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    object_id = models.PositiveIntegerField(
        verbose_name="related object",
        null=True,
    )

    content_object = GenericForeignKey("content_type", "object_id")

    primary_source = models.ForeignKey(
        PrimarySource, null=True, blank=True, on_delete=models.SET_NULL
    )
    text = models.TextField(blank=True)

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.__unicode__()


class Note(TimeStampedModel):
    # TODO: rename to SecondarySourceReference?
    note_type = models.ForeignKey(
        NoteType, default=1, null=True, on_delete=models.SET_NULL
    )
    secondary_source = models.ForeignKey(
        SecondarySource, null=True, on_delete=models.SET_NULL
    )

    text = models.TextField(blank=True)

    # useful to store the bookmark number, for instance
    extra_info = models.TextField(max_length=1024, blank=True)

    class Meta:
        abstract = True
        ordering = [
            "id",
        ]

    def __unicode__(self):
        return self.text.strip()

    def __str__(self):
        return self.__unicode__()


@with_author
class RelationshipAssertionReference(Note):
    """This is a SecondarySourceNote/Reference"""

    primary_source_references = GenericRelation(
        PrimarySourceReference,
        null=True,
        related_query_name="relationship_assertion_references",
    )

    def print_primary_source_refs(self):
        return ", ".join(
            [pref.__unicode__() for pref in self.primary_source_references.all()]
        )

    def url_to_edit_note(self):
        url = reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=[self.id],
        )
        return mark_safe('<a href="%s">%s</a>' % (url, self.__unicode__()))

    def related_label(self):
        return "[%s] %s (%s)<br><br>" % (
            self.secondary_source.abbrev_name,
            self.text,
            self.print_primary_source_refs(),
        )

    def __unicode__(self):
        return "%s, %s (%s)" % (
            self.secondary_source.abbrev_name,
            self.text,
            self.print_primary_source_refs(),
        )

    def __str__(self):
        return self.__unicode__()


@with_author
class PostAssertionNote(Note):
    def url_to_edit_note(self):
        url = reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=[self.id],
        )
        return mark_safe('<a href="%s">%s</a>' % (url, self.__unicode__()))

    def related_label(self):
        return "[%s - %s] %s <br>" % (
            self.note_type,
            self.secondary_source.abbrev_name,
            self.text,
        )


@with_author
class PersonNote(Note):
    def url_to_edit_note(self):
        url = reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=[self.id],
        )

        return mark_safe('<a href="%s">%s</a>' % (url, self.__unicode__()))

    def related_label(self):
        return "[%s - %s] %s<br><br>" % (
            self.note_type,
            self.secondary_source.abbrev_name,
            self.text,
        )

    def __str__(self):
        return self.__unicode__()


@with_author
class StatusAssertionNote(Note):
    def url_to_edit_note(self):
        url = reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=[self.id],
        )

        return mark_safe('<a href="%s">%s</a>' % (url, self.__unicode__()))

    def related_label(self):
        return "[%s - %s] %s<br><br>" % (
            self.note_type,
            self.secondary_source.abbrev_name,
            self.text,
        )

    def __str__(self):
        return self.__unicode__()


@with_author
class Person(TimeStampedModel):
    dprr_id = models.CharField(max_length=16, blank=True, null=True, unique=True)

    praenomen = models.ForeignKey(
        Praenomen, blank=True, null=True, on_delete=models.SET_NULL
    )
    praenomen_uncertain = models.BooleanField(
        verbose_name="Uncertain Praenomen", default=False
    )
    alt_praenomen = models.ForeignKey(
        Praenomen,
        blank=True,
        null=True,
        related_name="person_alt_praenomen_set",
        verbose_name="Alternative Praenomen",
        on_delete=models.SET_NULL,
    )

    nomen = models.CharField(max_length=128, blank=True)
    nomen_uncertain = models.BooleanField(verbose_name="Uncertain Nomen", default=False)

    cognomen = models.CharField(max_length=64, blank=True)
    cognomen_uncertain = models.BooleanField(
        verbose_name="Uncertain Cognomen", default=False
    )

    other_names = models.CharField(max_length=128, blank=True)
    other_names_uncertain = models.BooleanField(
        verbose_name="Uncertain Other Names", default=False
    )

    filiation = models.CharField(max_length=256, blank=True)
    filiation_uncertain = models.BooleanField(
        verbose_name="Uncertain Filiation", default=False
    )

    gentes = models.ManyToManyField(Gens, through="GensAssertion")

    tribes = models.ManyToManyField(Tribe, through="TribeAssertion")

    sex = models.ForeignKey(
        Sex, blank=True, null=True, default=1, on_delete=models.SET_NULL
    )

    re_number = models.CharField(max_length=32, blank=True, verbose_name="RE Number")
    re_number.help_text = "RE number"

    re_number_old = models.CharField(max_length=32, blank=True, verbose_name="RE (old)")
    re_number_old.help_text = "RE number before revising"

    origin = models.TextField(blank=True)

    patrician = models.BooleanField(verbose_name="Patrician", default=None, null=True)
    patrician_uncertain = models.BooleanField(
        verbose_name="Uncertain Patrician", default=False
    )
    patrician_notes = models.TextField(blank=True)

    novus = models.BooleanField(default=None, null=True)
    novus_uncertain = models.BooleanField(default=False)
    novus_notes = models.TextField(blank=True)

    nobilis = models.BooleanField(default=None, null=True)
    nobilis_uncertain = models.BooleanField(default=False)
    nobilis_notes = models.TextField(blank=True)

    extra_info = models.TextField(blank=True)
    extra_info.help_text = "Extra info about the person."

    notes = models.ManyToManyField(PersonNote, blank=True)

    # dates
    date_display_text = models.CharField(max_length=1024, blank=True, null=True)

    era_from = models.IntegerField(blank=False, null=False, default=0)
    era_to = models.IntegerField(blank=False, null=False, default=0)

    review_flag = models.BooleanField(verbose_name="Review needed", default=False)
    review_flag.help_text = "Person needs manual revision."

    review_notes = models.TextField(blank=True)

    highest_office = models.CharField(max_length=1024, blank=True, null=True)
    highest_office_edited = models.BooleanField(default=False)

    uncertain = models.BooleanField(default=False)

    class Meta:
        ordering = [
            "id",
        ]

    def __unicode__(self):  # noqa
        name_l = []

        # TODO: only showing praenomen for men
        if self.sex.name == "Male":
            if self.praenomen:
                prae_str = self.praenomen.abbrev

                if self.alt_praenomen:
                    prae_str += " (or {})".format(self.alt_praenomen.abbrev)
                elif self.praenomen_uncertain:
                    prae_str += "?"

                if prae_str.strip():
                    name_l.append(prae_str)

        if self.nomen:
            name_l.append(
                "{}{}".format(self.nomen, "?" if self.nomen_uncertain else "")
            )

        if self.re_number:
            name_l.append("({})".format(self.re_number))

        if self.filiation:
            if self.filiation not in ["- f. - n.", "- f.", "- n."]:
                name_l.append(
                    "{}".format(self.filiation, "?" if self.filiation_uncertain else "")
                )

        if self.tribeassertion_set.exists():
            name_l += [
                "{}{}".format(ta.tribe.abbrev, "?" if ta.uncertain else "")
                for ta in self.tribeassertion_set.all()
            ]

        if self.cognomen:
            name_l.append(
                "{}{}".format(self.cognomen, "?" if self.cognomen_uncertain else "")
            )

        if self.other_names:
            name_l.append(
                "{}{}".format(
                    self.other_names, "?" if self.other_names_uncertain else ""
                )
            )

        return " ".join(name_l)

    def generate_dprr_id(self):
        if not self.nomen:
            return None

        nomen = self.nomen.upper()

        if nomen[0] == "-":
            nomen = "ANON"

        if "(" in nomen:
            nomen = re.sub(r"\W", "", nomen)

        return "{}{:0>4}".format(nomen[:4], self.id)

    @property
    def f(self):
        return self._get_ancestor_praenomens(r"([^-].*?) f\..*")

    # Returns either the persons true highest Office
    # or false if no highest office existed.
    def get_real_highest_office(self):

        cos_list = [
            o.name
            for o in Office.objects.get(name="consul").get_descendants(
                include_self=True
            )
        ]

        pra_list = [
            o.name
            for o in Office.objects.get(name="praetor").get_descendants(
                include_self=True
            )
        ]

        aed_list = [
            o.name
            for o in Office.objects.get(name="aedilis").get_descendants(
                include_self=True
            )
        ]

        tri_list = [
            o.name
            for o in Office.objects.get(name="tribunus plebis").get_descendants(
                include_self=True
            )
        ]

        qua_list = [
            o.name
            for o in Office.objects.get(name="quaestor").get_descendants(
                include_self=True
            )
        ]

        cos_Q = Q(office__name__in=cos_list)
        pra_Q = Q(office__name__in=pra_list)
        aed_Q = Q(office__name__in=aed_list)
        tri_Q = Q(office__name__in=tri_list)
        qua_Q = Q(office__name__in=qua_list)

        pas = self.post_assertions.filter(
            cos_Q | pra_Q | aed_Q | tri_Q | qua_Q
        ).order_by("date_start")

        sas = self.statusassertion_set.all().order_by("date_start")

        if self.highest_office_edited:
            return self.highest_office
        elif pas.exists():
            cos = pas.filter(cos_Q)
            pra = pas.filter(pra_Q)
            aed = pas.filter(aed_Q)
            tri = pas.filter(tri_Q)
            qua = pas.filter(qua_Q)

            # TODO: test if any of these exist!!!
            if cos.exists():
                off = cos.first().office_str()
                date = cos.first().print_date()
            elif pra.exists():
                off = pra.first().office_str()
                date = pra.first().print_date()
            elif aed.exists():
                off = aed.first().office_str()
                date = aed.first().print_date()
            elif tri.exists():
                off = tri.first().office_str()
                date = tri.first().print_date()
            elif qua.exists():
                off = qua.first().office_str()
                date = qua.first().print_date()

            if not date:
                date = "uncertain date"

            if off and date:
                return "{} {}".format(off, date)
            else:
                return False

        elif sas.exists():
            off = sas.first().status.get_display_name()
            date = sas.first().date_start

            # See DPRR-385
            if off == "eq. R.":
                date = "?"
            elif date is not None:
                date = abs(date)
            else:
                date = "uncertain date"

            if off and date:
                return "{} {}".format(off, date)
            else:
                return False

        else:
            return False

    def _get_ancestor_praenomens(self, pattern):
        if not self.filiation:
            return None

        filiation = self.filiation.strip()

        found = re.search(pattern, filiation)

        if not found:
            return None

        praenomens = []
        text = found.groups()[0]
        text = self._split_name(text)

        for abbrev in text:
            # only need the content up to the first space
            abbrev = abbrev.split()[0]
            praenomens_qs = Praenomen.objects.filter(abbrev=abbrev)

            if praenomens_qs:
                p = praenomens_qs[0]
                praenomens.append(p.name)

                if p.has_alternate_name():
                    praenomens.append(p.alternate_name)

        return praenomens

    def _split_name(self, value):
        if not value:
            return None

        if " or " in value:
            return value.split(" or ")

        return [value]

    @property
    def n(self):
        return self._get_ancestor_praenomens(r"(?:.*\s+f\.\s+)?(.*[^-])\s+n\.")

    @property
    def other_names_plain(self):
        """Returns a plain version of the other names, without special
        characters or numbers."""
        if not self.other_names:
            return None

        other_names = self.other_names.strip()
        return re.sub(r"([^\w\.\s])|(\d+)", "", other_names).strip()

    def url_to_edit_person(self):
        url = reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=[self.id],
        )
        return mark_safe('<a href="{}">{}</a>'.format(url, self.__unicode__()))

    url_to_edit_person.short_description = "Person"

    def related_label(self):
        return mark_safe(self.url_to_edit_person())

    def has_status_information(self):
        return self.patrician or self.nobilis or self.novus or self.is_eques()

    def is_eques(self):
        return (
            self.statusassertion_set.filter(
                status__name__iexact=s.LOOKUPS["status"]["eques"]
            ).count()
            > 0
        )

    def get_eques_status_assertion(self):
        if not self.is_eques():
            return None

        return self.statusassertion_set.filter(
            status__name__iexact=s.LOOKUPS["status"]["eques"]
        ).first()

    def get_dates(self):
        if not self.dateinformation_set.all():
            return None

        date_qs = self.dateinformation_set.exclude(
            date_type__name=s.LOOKUPS["dates"]["person_exclude"]
        ).order_by("value")

        dates = list(date_qs)

        for index, item in enumerate(dates):
            if "death" in item.date_type.name:
                dates.insert(len(dates) - 1, dates.pop(index))

        return dates

    def get_career(self):
        if not self.post_assertions.all():
            return None

        return self.post_assertions.all().order_by("date_start")

    def get_reference_notes(self):
        return self.notes.filter(note_type=1)

    def __str__(self):
        return self.__unicode__()


@with_author
class TribeAssertion(TimeStampedModel):
    person = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)
    tribe = models.ForeignKey(
        Tribe, related_name="assertions", null=True, on_delete=models.SET_NULL
    )
    uncertain = models.BooleanField(verbose_name="Uncertain", default=False)

    secondary_source = models.ForeignKey(
        SecondarySource, blank=True, null=True, on_delete=models.SET_NULL
    )

    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Tribe"

    def __unicode__(self):
        return "{}{}".format(self.tribe.abbrev, "?" if self.uncertain else "")

    def __str__(self):
        return self.__unicode__()


@with_author
class GensAssertion(TimeStampedModel):
    person = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)
    gens = models.ForeignKey(
        Gens, related_name="assertions", null=True, on_delete=models.SET_NULL
    )
    uncertain = models.BooleanField(default=False)

    secondary_source = models.ForeignKey(
        SecondarySource, blank=True, null=True, on_delete=models.SET_NULL
    )

    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Gens"
        verbose_name_plural = "Gentes"

    def __unicode__(self):
        return "{}{}".format(self.gens.name, " ?" if self.uncertain else "")

    def __str__(self):
        return self.__unicode__()


@with_author
class DateType(TimeStampedModel):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return "%s" % self.name

    def __str__(self):
        return self.__unicode__()


@with_author
class DateInformation(TimeStampedModel):
    person = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)

    SINGLE = "S"
    INTERVAL_CHOICES = ((SINGLE, "Single"), ("B", "Before"), ("A", "After"))

    date_type = models.ForeignKey(
        DateType,
        related_name="person_date",
        verbose_name="Type",
        null=True,
        on_delete=models.SET_NULL,
    )
    date_interval = models.CharField(
        max_length=1, choices=INTERVAL_CHOICES, default=SINGLE, verbose_name="Interval"
    )
    uncertain = models.BooleanField(default=False)
    value = models.IntegerField()

    secondary_source = models.ForeignKey(
        SecondarySource, blank=True, null=True, on_delete=models.SET_NULL
    )
    source_text = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Date"

    def __unicode__(self):
        date_str = ""

        if self.value >= 0:
            date_str = "A.D. "

        date_str += str(abs(self.value))

        if self.uncertain:
            date_str += "?"

        label = self.get_date_interval_display()
        label = label if label != self.INTERVAL_CHOICES[0][1] else ""

        di_str = "{} {}, {}".format(label, date_str, self.date_type)

        if self.secondary_source:
            di_str += " ({})".format(self.secondary_source)

        return di_str

    def __str__(self):
        return self.__unicode__()

    def has_ruepke_secondary_source(self):
        if not self.secondary_source:
            return False

        return (
            self.secondary_source.abbrev_name.lower()
            == s.LOOKUPS["notes"]["ruepke_source"]
        )

    def get_ruepke_notes(self):
        if not self.has_ruepke_secondary_source():
            return None

        texts = [
            note.text
            for note in self.person.notes.filter(
                note_type__name=s.LOOKUPS["notes"]["date_information_source"]
            )
        ]

        return ", ".join(texts)


@with_author
class Office(MPTTModel, TimeStampedModel):
    name = models.CharField(max_length=256, unique=True)
    abbrev_name = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=1024, blank=True)

    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name_plural = "Office"
        verbose_name = "Office"
        ordering = ["tree_id", "lft", "name"]

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __unicode__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return (
            "id__iexact",
            "name__icontains",
        )

    def __str__(self):
        return self.__unicode__()


@with_author
class RelationshipType(TimeStampedModel):
    name = models.CharField(max_length=256, unique=True)
    order = models.PositiveSmallIntegerField(default=0)
    description = models.CharField(max_length=1024, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


@with_author
class Province(MPTTModel, TimeStampedModel):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)

    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name_plural = "Provinces"
        verbose_name = "Province"
        ordering = ["tree_id", "lft", "name"]

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


@with_author
class PostAssertion(TimeStampedModel):
    person = models.ForeignKey(
        Person, related_name="post_assertions", null=True, on_delete=models.SET_NULL
    )
    office = models.ForeignKey(Office, null=True, on_delete=models.SET_NULL)

    secondary_source = models.ForeignKey(
        SecondarySource, null=True, on_delete=models.SET_NULL
    )

    provinces = models.ManyToManyField(
        Province, blank=True, through="PostAssertionProvince"
    )
    province_original = models.CharField(max_length=512, blank=True)
    province_original_expanded = models.CharField(max_length=512, blank=True)

    original_text = models.CharField(max_length=1024, blank=True)
    office_xref = models.CharField(max_length=1024, blank=True)

    uncertain = models.BooleanField(verbose_name="Uncertain", default=False)
    unknown = models.BooleanField(default=False)

    notes = models.ManyToManyField(PostAssertionNote, blank=True)

    # position field
    # used to set order in inline position
    position = models.PositiveSmallIntegerField(default=0)

    # date information
    date_start = models.IntegerField(blank=True, null=True)
    date_start_uncertain = models.BooleanField(default=False)

    date_end = models.IntegerField(blank=True, null=True)
    date_end_uncertain = models.BooleanField(default=False)

    date_display_text = models.CharField(max_length=1024, blank=True, null=True)
    date_source_text = models.CharField(max_length=1024, blank=True, null=True)
    date_secondary_source = models.ForeignKey(
        SecondarySource,
        blank=True,
        null=True,
        related_name="postassertion_date_secondary_source",
        on_delete=models.SET_NULL,
    )

    review_flag = models.BooleanField(verbose_name="Review needed", default=False)
    review_flag.help_text = "Manual revision needed."

    class Meta:
        ordering = [
            "-date_end",
            "-date_start",
        ]

    def office_str(self):
        """returns the office name, using the abbreviated version
        also includes a question mark if uncertain"""

        name = ""

        if self.office.abbrev_name != "":
            name = self.office.abbrev_name
        else:
            name = self.office.name

        if self.uncertain:
            name = "{}?".format(name)

        return name

    def __unicode__(self):

        off = "No office"
        if self.office:
            off = self.office.__unicode__()

        name = str(self.person.__unicode__()) + ": " + off + " " + self.print_date()

        name = name + " (" + self.secondary_source.abbrev_name + ")"
        return name

    def __str__(self):
        return self.__unicode__()

    def print_provinces(self):
        provinces = []

        if self.id:
            for prov in self.postassertionprovince_set.all():
                name = str(prov.province)
                if prov.uncertain:
                    name = name + "?"

                provinces.append(name)

        return mark_safe(", ".join(provinces))

    print_provinces.short_description = "Provinces"

    def print_date(self):  # noqa
        """returns a friendly version of the post assertion dates"""

        # So where the post has uncertain start and certain end,
        #    this represents 'before' the end date plus 1.
        # e.g.
        # start date = -91 uncertain, end date = -91 certain means 'before 90'.
        # start date = -91 certain, end date = -91 uncertain means 'after 92'.
        # start date = 91 = end date, both uncertain means 'c. 91'.

        date_str = ""

        if self.date_display_text:
            return self.date_display_text

        elif self.date_start == self.date_end:
            # single value dates
            # safe to convert, all dates are negative
            if self.date_start is None:
                return "date uncertain"

            date_val = abs(self.date_start)

            if self.date_start_uncertain and not self.date_end_uncertain:
                date_str = "before {}".format(date_val - 1)
            elif not self.date_start_uncertain and self.date_end_uncertain:
                date_str = "after {}".format(date_val + 1)
            elif self.date_start_uncertain and self.date_end_uncertain:
                date_str = "c. {}".format(date_val)
            else:
                date_str = str(date_val)

        else:
            st = ""
            en = ""
            # if both dates differ, we need to print the interval
            if self.date_start:
                st = str(abs(int(self.date_start)))

                if self.date_start_uncertain:
                    st = "before {}".format(st)

            if self.date_end:
                en = str(abs(self.date_end))

                if self.date_end_uncertain:
                    en = "after {}".format(en)

            if st and en:
                date_str = "{} to {}".format(st, en)
            elif st:
                if self.date_start_uncertain:
                    # Already taken care of above
                    date_str = st
                else:
                    date_str = "after {}".format(st)
            elif en:
                if self.date_end_uncertain:
                    # Alreadt taken care of above
                    date_str = en
                else:
                    date_str = "before {}".format(en)
            else:
                date_str = "date uncertain"

        return date_str.strip()

    def has_ruepke_secondary_source(self):
        if not self.secondary_source:
            return False

        return (
            self.secondary_source.abbrev_name.lower()
            == s.LOOKUPS["notes"]["ruepke_source"]
        )

    def get_ruepke_notes(self):
        if not self.has_ruepke_secondary_source():
            return None

        texts = [
            note.text
            for note in self.person.notes.filter(
                note_type__name=s.LOOKUPS["notes"]["post_assertion_source"]
            )
        ]

        return ", ".join(texts)


@with_author
class PostAssertionProvince(models.Model):
    post_assertion = models.ForeignKey(
        PostAssertion, null=True, on_delete=models.SET_NULL
    )
    province = models.ForeignKey(Province, null=True, on_delete=models.SET_NULL)
    uncertain = models.BooleanField(verbose_name="Uncertain", default=False)
    note = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        un = ""
        if self.uncertain:
            un = "?"

        return self.province.name + " " + un

    def __str__(self):
        return self.__unicode__()


@with_author
class RelationshipAssertion(TimeStampedModel):
    person = models.ForeignKey(
        Person,
        related_name="relationships_as_subject",
        null=True,
        on_delete=models.SET_NULL,
    )
    relationship = models.ForeignKey(
        RelationshipType, null=True, on_delete=models.SET_NULL
    )
    related_person = models.ForeignKey(
        Person,
        related_name="relationships_as_object",
        null=True,
        on_delete=models.SET_NULL,
    )

    # relationship number indicates if it's the third wife of
    relationship_number = models.PositiveSmallIntegerField(null=True, blank=True)
    # when referring to the third wife of it's also useful to link to the other
    # relationship - in this case the previous
    related_relationship = models.ForeignKey(
        "self", null=True, blank=True, related_name="next", on_delete=models.SET_NULL
    )

    # when two different sources write about the two sides of the relationship
    # this field indicates that one is the inverse of the other
    inverse_relationship = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )

    uncertain = models.BooleanField(verbose_name="Uncertain", default=False)

    original_text = models.CharField(max_length=1024, blank=True)

    # TODO: should this be removed - and use the Note instead?
    secondary_source = models.ForeignKey(
        SecondarySource, null=True, on_delete=models.SET_NULL
    )

    # TODO: normalise - same as PostAssertionNotes
    references = models.ManyToManyField(RelationshipAssertionReference, blank=True)

    extra_info = models.TextField(blank=True)
    extra_info.help_text = "Extra info about the relationship"

    review_flag = models.BooleanField(verbose_name="Review needed", default=False)

    def __unicode__(self):
        return "{} is {} {}".format(self.person, self.relationship, self.related_person)

    def __str__(self):
        return self.__unicode__()

    # flag indicates that the Status Assertion was manually verified
    # and should not be edited/deleted automatically
    is_verified = models.BooleanField(verbose_name="Editor Verified", default=False)

    # Return the inverse of the objects
    # relationship type based on gender of people
    def get_inverse_relationship(self):
        try:
            return RelationshipInverse.objects.get(
                relationship=self.relationship, sex=self.related_person.sex
            )
        except Exception:
            return None

    class Meta:
        ordering = ["relationship__order", "relationship_number", "id"]


class RelationshipInverse(models.Model):
    relationship = models.ForeignKey(
        RelationshipType, null=True, on_delete=models.SET_NULL
    )
    sex = models.ForeignKey(Sex, null=True, on_delete=models.SET_NULL)
    inverse_relationship = models.ForeignKey(
        RelationshipType, related_name="inverse", null=True, on_delete=models.SET_NULL
    )


@with_author
class StatusType(TimeStampedModel):
    name = models.CharField(max_length=256, unique=True)
    abbrev_name = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return "{}".format(self.name)

    def __str__(self):
        return self.__unicode__()

    def get_display_name(self):
        if self.abbrev_name:
            return self.abbrev_name

        return self.name


@with_author
class StatusAssertion(TimeStampedModel):
    person = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)
    status = models.ForeignKey(StatusType, null=True, on_delete=models.SET_NULL)
    secondary_source = models.ForeignKey(
        SecondarySource, null=True, on_delete=models.SET_NULL
    )

    uncertain = models.BooleanField(verbose_name="Uncertain", default=False)
    original_text = models.CharField(max_length=1024, blank=True)

    extra_info = models.TextField(blank=True)
    extra_info.help_text = "Extra info about the status assertion"

    review_flag = models.BooleanField(verbose_name="Review needed", default=False)

    # flag indicates that the Status Assertion was manually verified
    #   and should not be edited/deleted automatically
    #   used by add_senator_data script to create new senator StatusAssertions
    is_verified = models.BooleanField(verbose_name="Editor Verified", default=False)

    # date information
    date_start = models.IntegerField(blank=True, null=True)
    date_start_uncertain = models.BooleanField(default=False)

    date_end = models.IntegerField(blank=True, null=True)
    date_end_uncertain = models.BooleanField(default=False)

    date_display_text = models.CharField(max_length=1024, blank=True, null=True)

    date_source_text = models.CharField(max_length=1024, blank=True, null=True)
    date_secondary_source = models.ForeignKey(
        SecondarySource,
        blank=True,
        null=True,
        related_name="date_source",
        on_delete=models.SET_NULL,
    )

    # province information
    provinces = models.ManyToManyField(
        Province, blank=True, through="StatusAssertionProvince"
    )

    # notes
    notes = models.ManyToManyField(StatusAssertionNote, blank=True)

    def print_date(self):  # noqa
        """returns a friendly version of the post assertion dates"""

        # So where the post has uncertain start and certain end,
        #    this represents 'before' the end date plus 1.
        # e.g.
        # start date = -91 uncertain, end date = -91 certain means 'before 90'.
        # start date = -91 certain, end date = -91 uncertain means 'after 92'.
        # start date = 91 = end date, both uncertain means 'c. 91'.

        date_str = ""

        if self.date_display_text:
            return self.date_display_text

        elif self.date_start == self.date_end:
            # single value dates
            # safe to convert, all dates are negative
            if self.date_start is None:
                return "date uncertain"

            date_val = abs(self.date_start)

            if self.date_start_uncertain and not self.date_end_uncertain:
                date_str = "before {}".format(date_val - 1)
            elif not self.date_start_uncertain and self.date_end_uncertain:
                date_str = "after {}".format(date_val + 1)
            elif self.date_start_uncertain and self.date_end_uncertain:
                date_str = "c. {}".format(date_val)
            else:
                date_str = str(date_val)

        else:
            st = ""
            en = ""
            # if both dates differ, we need to print the interval
            if self.date_start:
                st = str(abs(int(self.date_start)))

                if self.date_start_uncertain:
                    st = "before {}".format(st)

            if self.date_end:
                en = str(abs(self.date_end))

                if self.date_end_uncertain:
                    en = "after {}".format(en)

            if st and en:
                date_str = "{} to {}".format(st, en)
            elif st:
                if self.date_start_uncertain:
                    # Already taken care of above
                    date_str = st
                else:
                    date_str = "after {}".format(st)
            elif en:
                if self.date_end_uncertain:
                    # Alreadt taken care of above
                    date_str = en
                else:
                    date_str = "before {}".format(en)
            else:
                date_str = "date uncertain"

        return date_str.strip()

    # we need to use the connecting table unicode method in order to print
    #  uncertainty info, etc.
    def print_provinces(self):
        pl = [p.__unicode__() for p in self.statusassertionprovince_set.all()]
        return mark_safe(", ".join(pl))

    print_provinces.short_description = "Provinces"

    def __unicode__(self):
        return "{} {}{} {} ({})".format(
            self.person,
            self.status,
            "?" if self.uncertain else "",
            self.print_date(),
            self.secondary_source.abbrev_name,
        )

    def __str__(self):
        return self.__unicode__()


@with_author
class StatusAssertionProvince(models.Model):
    status_assertion = models.ForeignKey(
        StatusAssertion, null=True, on_delete=models.SET_NULL
    )
    province = models.ForeignKey(Province, null=True, on_delete=models.SET_NULL)
    uncertain = models.BooleanField(verbose_name="Uncertain", default=False)
    note = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        un = ""
        if self.uncertain:
            un = "?"

        return self.province.name + " " + un

    def __str__(self):
        return self.__unicode__()
