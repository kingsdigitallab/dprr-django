#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django_mptt_admin.admin import DjangoMpttAdmin
from django.contrib.contenttypes import generic
from django.forms import TextInput, Textarea

from models import Person, Office, Praenomen, AssertionPerson, \
    Assertion, AssertionType, RoleType, DateType, \
    SecondarySource, Gens, AssertionNote, AssertionPersonNote, \
    Tribe, AssertionDate, PersonDate, AssertionPersonDate, AssertionNoteThrough

admin.site.register(AssertionType)
admin.site.register(DateType)
admin.site.register(RoleType)
admin.site.register(AssertionDate)
admin.site.register(AssertionPersonDate)


# Date Inline Admin
class DateInline(admin.StackedInline):
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)

    readonly_fields = ('id', )
    fields = (['id', 'date_type'], ['interval', 'year', ], ['circa', 'year_uncertain', ], 'extra_info')
    extra = 0

    show_change_link = True

class AssertionDateInline(DateInline):
    verbose_name = 'Assertion Date'
    verbose_name_plural = 'Assertion Dates'

    model = AssertionDate

class AssertionPersonDateInline(DateInline):
    verbose_name = 'Assertion Person Date'
    verbose_name_plural = 'Assertion Person Dates'

    model = AssertionPersonDate

class PersonDateInline(DateInline):
    verbose_name = 'Person Date'
    verbose_name_plural = 'Person Dates'

    model = PersonDate


class AssertionPersonNoteInline(admin.StackedInline):
    model = AssertionPerson.notes.through
    extra = 0

    raw_id_fields = ['assertionperson']

    related_lookup_fields = {
        'm2m': 'assertionperson'
        }


# TODO: not displaying all info...
class AssertionPersonAdmin(admin.ModelAdmin):

    fieldsets = [
            ('Database Info', {'fields': [('id')]}),
            ('', {'fields': ['assertion', 'person']}),
            ]

    readonly_fields = ('id', )
    list_display = ('id', 'assertion', 'person', 'created_by', 'created', 'modified')

    # fields = (['id', ])

    raw_id_fields = ('assertion', 'person', )

    related_lookup_fields = {
         'fk': ['assertion', 'person'],
    }

    inlines = (AssertionPersonDateInline, AssertionPersonNoteInline, )

admin.site.register(AssertionPerson, AssertionPersonAdmin)


class AssertionInline(admin.StackedInline):
    model = Assertion.persons.through

    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)

    verbose_name = 'Assertion'
    verbose_name_plural = 'Person Assertions'

    fields = (['assertion', 'role'],  ['original_text', 'office_xref'], 'notes')
    extra = 0

    raw_id_fields = ('notes', 'assertion')

    related_lookup_fields = {
        'pk': ['assertion', ],
        'm2m': ['notes', ],
    }


class AssertionNoteInline(admin.StackedInline):
    model = AssertionNoteThrough

    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)

    verbose_name = 'Assertion Note'
    verbose_name_plural = 'Assertion Notes'

    readonly_fields = ('_note_type', )

    raw_id_fields = ('assertionnote', )

    related_lookup_fields = {
        'm2m': ['assertionnote'],
    }

    def _note_type(self, obj):
        return obj.assertionnote.get_note_type_display()

    # readonly_fields = ('id', )

    extra = 0
    show_change_link = True


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'note_type', 'secondary_source', 'text', 'extra_info', 'created', 'modified')
    list_display_links = ('note_type', 'secondary_source', 'text', 'extra_info')
    readonly_fields = ('id', 'created', 'modified')

    search_fields = ['id', 'note_type', 'text']
    fields = ('id', ['secondary_source', 'note_type'], 'text', 'extra_info', )

    # list_display_links = ('id', 'certainty', 'assertion_type', 'office', 'secondary_source')

    show_change_link = True


admin.site.register(AssertionPersonNote, NoteAdmin)
admin.site.register(AssertionNote, NoteAdmin)


class PersonInline(admin.StackedInline):

    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)

    verbose_name_plural = 'Persons on this Assertion'
    verbose_name = 'Person:'

    show_change_link = True

    model = Assertion.persons.through

    fields = (['id', 'position'] , ['person', 'role'],  ['original_text', 'office_xref'], 'notes')
    sortable_field_name = 'position'

    readonly_fields = ('id', )

    raw_id_fields = ('person', 'notes')
    related_lookup_fields = {
        'fk': ['person', ],
        'm2m': ['notes', ]
    }

    extra = 0

    # autocomplete_lookup_fields = {
    #     'm2m': ['person', 'assertion', ],
    # }



class AssertionYearListFilter(SimpleListFilter):
    title = 'assertion year'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        lookup = []
        years = Assertion.objects.all().values('date__year').distinct()

        for year in years:
            item = (year['date__year'], year['date__year'])
            if item not in lookup:
                lookup.append(item)

        return sorted(lookup)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(date__year__exact=self.value())


class PersonAdmin(admin.ModelAdmin):

    fieldsets = [
            ('Database Info', {'fields': [('id', 'review_flag')]},),
            ('Person',
                 {'fields': [
            ('praenomen', 'filiation', ),
            ('nomen',),
            ('cognomen', 'other_names'),
            ('gens', 'tribe', 'origin'),
            ('sex',),
        ]}),

        ('RE',
            {'fields': [
                ('real_number', 'real_number_old', ),
            ]}
        ),
        ('Other', {'fields': [('patrician', 'patrician_certainty')]})]

    readonly_fields = ('id', )
    list_display = (
        'id',
        'url_to_edit_person',
        'review_flag',
        'updated_by',
        'modified',
        'created_by',
        'created',
        )

    search_fields = ['nomen', 'cognomen', 'praenomen__abbrev', 'praenomen__name', 'other_names', ]

    list_filter = ('assertionperson__role', 'nomen', 'assertionperson__assertion__office', 'review_flag', )

    inlines = (PersonDateInline, AssertionInline, )
    exclude = ('assertions',  )


admin.site.register(Person, PersonAdmin)

class OfficeAdmin(DjangoMpttAdmin):
    readonly_fields = ('id', )
    mptt_indent_field = "name"

    list_display = (
        'id',
        'name',
        'description',
        )

admin.site.register(Office, OfficeAdmin)




class AssertionAdmin(admin.ModelAdmin):

    search_fields = ['assertionperson__person__nomen', 'assertionperson__person__cognomen', ]
    list_filter = ('secondary_source', 'assertion_type', AssertionYearListFilter, 'office')

    list_display = (
        'id',
        'assertion_type',
        'office',
        'get_dates',
        'secondary_source',
        'certainty',
        'modified',
        'created',
    )

    readonly_fields = ('id', )
    list_display_links = ('id', 'certainty', 'assertion_type', 'office', 'secondary_source')

    raw_id_fields = ('office', )
    related_lookup_fields = {
        'fk': ['office', ],
    }

    fieldsets = [
                    ('Database Info', {'fields': ['id']}),
                    ('Assertion',
                        {
                        'fields': [
                                ('secondary_source', 'certainty', ),
                                ('assertion_type', 'office',),
                                ],
                        'classes': ('grp-collapse grp-open',),
                        }
                    ),
            ]

    inlines = [AssertionDateInline, PersonInline, AssertionNoteInline, ]
    exclude = ('persons',  )

admin.site.register(Assertion, AssertionAdmin)



class GensAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', )
    readonly_fields = ('id', )
    list_display_links = ('id', 'name', )

admin.site.register(Gens, GensAdmin)


class TribeAdmin(admin.ModelAdmin):

    list_display = ('id', 'abbrev', 'name', )
    readonly_fields = ('id', )
    list_display_links = ('id', 'abbrev', 'name', )

admin.site.register(Tribe, TribeAdmin)


class PraenomenAdmin(admin.ModelAdmin):

    list_display = ('id', 'abbrev', 'name')
    readonly_fields = ('id', )
    list_display_links = ('id', 'abbrev', 'name')


admin.site.register(Praenomen, PraenomenAdmin)


class SecondarySourceAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'abbrev_name', 'biblio')
    readonly_fields = ('id', )
    list_display_links = ('id', 'abbrev_name', 'name', 'biblio')


admin.site.register(SecondarySource, SecondarySourceAdmin)


