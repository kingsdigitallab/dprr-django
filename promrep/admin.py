#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django.contrib.contenttypes import generic

from models import Person, Office, Praenomen, AssertionPerson, \
    Assertion, AssertionType, RoleType, Date, DateType, Certainty, \
    SecondarySource

admin.site.register(AssertionType)
admin.site.register(Date)
admin.site.register(DateType)
admin.site.register(RoleType)


class PersonInline(admin.TabularInline):

    model = Assertion.persons.through

    fields = ('id', 'person', 'role', 'assertion', 'original_text')
    readonly_fields = ('id', 'assertion', 'person')
    extra = 0


class PersonDateInline(generic.GenericStackedInline):

    model = Date
    extra = 0


class AssertionDateInline(generic.GenericStackedInline):

    model = Date
    extra = 0


class PersonAdmin(admin.ModelAdmin):

    fieldsets = [('Database Info', {'fields': ['id']}), ('Person',
                 {'fields': [
        'original_text',
        'sex',
        'praenomen',
        'nomen',
        ('cognomen_first', 'cognomen_other'),
        'filiation',
        ]}), ('Real', {'fields': ['real_number', 'real_number_old',
              'real_attribute']}), ('Other', {'fields': [('is_noble',
                                    'noble_certainty'), ('is_novus_homo'
                                    , 'novus_homo_certainty'),
                                    ('is_patrician',
                                    'patrician_certainty')]})]

    readonly_fields = ('id', 'original_text')
    list_display = (
        'id',
        'url_to_edit_person',
        'sex',
        'get_dates',
        'is_noble',
        'is_novus_homo',
        'is_patrician',
        'notes',
        'modified',
        'created',
        )

    inlines = (PersonInline, PersonDateInline)


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

    list_display = (
        'id',
        'assertion_type',
        'get_persons',
        'assertion_type',
        'office',
        'display_text',
        'secondary_source',
        'modified',
        'created',
        )

    list_display_links = ('id', 'display_text')
    readonly_fields = ('id', )

    inlines = [PersonInline, AssertionDateInline]
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
