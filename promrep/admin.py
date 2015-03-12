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
admin.site.register(AssertionPerson)
admin.site.register(AssertionDate)
admin.site.register(AssertionPersonDate)


class AssertionInline(admin.StackedInline):
    model = Assertion.persons.through

    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)

    verbose_name = 'Assertion'
    verbose_name_plural = 'Person Assertions'

    fields = (['assertion', 'role'],  ['original_text', 'office_xref'], 'notes')
    raw_id_fields = ('assertion', 'notes', )

    extra = 0

#    autocomplete_lookup_fields = {
#        'm2m': ['notes', ],
#    }

    show_change_link = True

    raw_id_fields = ('notes',)

    related_lookup_fields = {
        'm2m': ['notes'],
    }


class AssertionDateInline(admin.StackedInline):
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)

    verbose_name = 'Assertion Date'
    verbose_name_plural = 'Assertion Dates'

    model = AssertionDate

    readonly_fields = ('id', )
    fields = (['id', 'date_type'], ['interval', 'year', ], ['circa', 'year_uncertain', ], 'extra_info')
    extra = 0

    show_change_link = True


class AssertionNoteInline(admin.StackedInline):
    model = AssertionNoteThrough

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


class AssertionPersonNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'note_type', 'text', 'created', 'modified')

    readonly_fields = ('id', 'created', 'modified')
    fields = ('id', 'note_type', 'text', 'extra_info', )

admin.site.register(AssertionPersonNote, AssertionPersonNoteAdmin)


class AssertionNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'note_type', 'text', 'extra_info', 'created', 'modified')
    readonly_fields = ('id', 'created', 'modified')

    search_fields = ['id', 'note_type', 'text']
    fields = ('id', 'note_type', 'text', 'extra_info', )

admin.site.register(AssertionNote, AssertionNoteAdmin)


class PersonInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    verbose_name = 'Assertion Person'
    verbose_name_plural = 'Assertion-Person Relationships'

    show_change_link = True

    model = Assertion.persons.through

    fields = ('person', 'role', 'original_text', 'position', )
    sortable_field_name = "position"

    readonly_fields = ('id', )

    raw_id_fields = ('person', )

    related_lookup_fields = {
        'fk': ['person'],
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

    inlines = (AssertionInline, )

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
    raw_id_fields = ('office', 'secondary_source', 'assertion_type', )
    list_display_links = ('id', 'certainty', 'assertion_type', 'office', 'secondary_source')

    autocomplete_lookup_fields = {
        'fk': ['office', 'secondary_source', 'assertion_type', ],
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


