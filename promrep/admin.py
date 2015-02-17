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
    Tribe, AssertionDate, PersonDate, AssertionPersonDate

admin.site.register(AssertionType)
admin.site.register(DateType)
admin.site.register(RoleType)
admin.site.register(AssertionNote)
admin.site.register(AssertionPersonNote)
admin.site.register(AssertionPerson)

# these two classes are separated to allow better field configuration
class AssertionInline(admin.TabularInline):
    verbose_name = 'Assertion'
    verbose_name_plural = 'Assertions'

    model = Assertion.persons.through

    fields = ('assertion', 'role',  'original_text', )

    raw_id_fields = ('assertion', )
    extra = 0

    # autocomplete_lookup_fields = {
    #     'm2m': ['assertion', ],
    # }

class AssertionDateInline(admin.TabularInline):
    verbose_name = 'Assertion Date'
    verbose_name = 'Assertion Dates'

    model = Assertion.dates.through
    exclude = ('assertions',)

    readonly_fields = ('id', )
    extra = 0

    show_change_link = True


class AssertionNoteInline(admin.TabularInline):
    verbose_name = 'Note'
    verbose_name = 'Notes'

    model = Assertion.notes.through

    readonly_fields = ('id', )
    extra = 0

    show_change_link = True


class PersonInline(admin.TabularInline):
    verbose_name = 'Person'
    verbose_name_plural = 'Persons'

    show_change_link = True

    model = Assertion.persons.through

    fields = ('person', 'role', 'original_text', )
    readonly_fields = ('id', )

    raw_id_fields = ('person', )
    extra = 0

    # autocomplete_lookup_fields = {
    #     'm2m': ['person', 'assertion', ],
    # }



class AssertionYearListFilter(SimpleListFilter):
    title = 'assertion year'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        lookup = []
        years = Assertion.objects.all().values('dates__year').distinct()

        for year in years:
            lookup.append((year['dates__year'], year['dates__year']))

        return sorted(lookup)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(dates__year__exact=self.value())


class PersonAdmin(admin.ModelAdmin):

    fieldsets = [('Database Info', {'fields': ['id']}), ('Person',
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
                 'real_attribute',
            ]}
        ),
        ('Other', {'fields': [('patrician', 'patrician_certainty')]})]

    readonly_fields = ('id', )
    list_display = (
        'id',
        'url_to_edit_person',
        'tribe',
        'gens',
        'origin',
        'sex',
        'get_dates',
        'patrician',
        'patrician_certainty',
        'modified',
        'created',
        )

    search_fields = ['nomen', 'cognomen', 'tribe']
    list_filter = ('assertionperson__role', 'assertionperson__assertion__office', 'tribe__name', 'tribe__abbrev')

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
        'display_text',
        'secondary_source',
        )

    list_display_links = ('id', 'get_dates', 'display_text', 'assertion_type', 'office', 'secondary_source')
    readonly_fields = ('id', )

    raw_id_fields = ('office', 'secondary_source', 'assertion_type', )

    autocomplete_lookup_fields = {
        'fk': ['office', 'secondary_source', 'assertion_type', ],
    }

    fieldsets = [('Database Info', {'fields': ['id']}),
    ('Assertion', {'fields': [
            ('secondary_source', ),
            ('assertion_type', 'office',),
            ]}),]

    inlines = [AssertionDateInline, PersonInline, AssertionNoteInline]
    exclude = ('persons', )

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


