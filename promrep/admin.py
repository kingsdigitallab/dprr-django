#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from mptt.admin import MPTTModelAdmin
from django.contrib.contenttypes import generic
from django.forms import TextInput, Textarea

from models import Person, Office, Praenomen, AssertionPerson, \
    Assertion, AssertionType, RoleType, Date, DateType, Certainty, \
    SecondarySource

admin.site.register(AssertionType)
admin.site.register(Date)
admin.site.register(DateType)
admin.site.register(RoleType)


class AssertionPersonInline(admin.StackedInline):
    verbose_name = ''
    verbose_name_plural = 'Assertions on this person'

    model = Assertion.persons.through

    fields = ('id', 'person', 'role', 'assertion', 'original_text')
    readonly_fields = ('id', )

    raw_id_fields = ('person', 'assertion', )
    extra = 0

class PersonDateInline(generic.GenericStackedInline):

    model = Date
    extra = 0


class AssertionDateInline(generic.GenericStackedInline):

    model = Date
    extra = 0


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
        'original_text',
        'sex',
        'praenomen',
        'nomen',
        ('cognomen_first', 'cognomen_other'),
        'filiation',
        ]}),
        ('Real', {'fields': ['real_number', 'real_number_old',
              'real_attribute']}), ('Other', {'fields': [('consular_ancestor',
                                    'consular_ancestor_certainty'), ('novus_homo'
                                    , 'novus_homo_certainty'),
                                    ('is_patrician',
                                    'patrician_certainty')]})]

    readonly_fields = ('id', 'original_text')
    list_display = (
        'id',
        'url_to_edit_person',
        'sex',
        'get_dates',
        'consular_ancestor',
        'novus_homo',
        'is_patrician',
        'notes',
        'modified',
        'created',
        )

    search_fields = ['nomen', 'cognomen_first', ]
    list_filter = ('assertionperson__role', 'assertionperson__assertion__office',)

    inlines = (AssertionPersonInline, PersonDateInline,)


admin.site.register(Person, PersonAdmin)


class OfficeAdmin(MPTTModelAdmin):

    readonly_fields = ('id', )
    list_display = (
        'id',
        'name',
        'parent',
        'description',
        'modified',
        'created',
        )


admin.site.register(Office, OfficeAdmin)


class AssertionAdmin(admin.ModelAdmin):

    search_fields = ['assertionperson__person__nomen', 'assertionperson__person__cognomen_first', ]
    list_filter = ('secondary_source', 'assertion_type', AssertionYearListFilter)

    list_display = (
        'id',
        'assertion_type',
        'office',
        'get_persons',
        'get_dates',
        'display_text',
        'notes',
        'secondary_source',
        )

    list_display_links = ('id', 'get_persons', 'get_dates', 'display_text', 'notes')
    readonly_fields = ('id', )

    inlines = [AssertionPersonInline, AssertionDateInline, ]
    exclude = ('persons', )


admin.site.register(Assertion, AssertionAdmin)


class CertaintyAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description')
    readonly_fields = ('id', )
    list_display_links = ('id', 'name', 'description')


admin.site.register(Certainty, CertaintyAdmin)


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


