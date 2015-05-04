#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django_mptt_admin.admin import DjangoMpttAdmin
from django.contrib.contenttypes import generic
from django.forms import TextInput, Textarea

from django.core import urlresolvers
from django.utils.html import format_html

from promrep.forms import PostInlineForm

from models import Person, Office, Praenomen, PostAssertion, \
    Post, RoleType, DateType, SecondarySource, Gens, PostNote, \
    PostAssertionNote, Tribe, Location

admin.site.register(DateType)
admin.site.register(RoleType)

class PostAssertionNoteInline(admin.StackedInline):
    model = PostAssertion.notes.through
    extra = 0

    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

    verbose_name = 'Post Person Note'
    verbose_name_plural = 'Post Person Notes'

    raw_id_fields = ('postassertionnote', )

    related_lookup_fields = {
        'fk': ['postassertionnote', ],
    }


class PostAssertionAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'person',
                    'date_start', 'date_end', 'secondary_source', 'review_flag',
                    'created_by', 'created', 'modified')

    readonly_fields = ('id', )

    fieldsets = [
            ('Database Info',
                {'fields': [('id', 'review_flag'), ]}),
            ('', {'fields':
                    [
                        'person',
                        'post',
                        ('role', 'uncertain'),
                        ('original_text', 'office_xref'),
                    ],
                }
                ),
            ('Dates', {'fields': [
                        ('date_display_text'),
                        ('date_source_text', 'date_secondary_source'),
                        ('date_start', 'date_start_uncertain'),
                        ('date_end', 'date_end_uncertain')
                     ]})
            ]

    raw_id_fields = ('post', 'person',  )

    related_lookup_fields = {
         'fk': ['post', 'person'],
    }

    inlines = (PostAssertionNoteInline, )

admin.site.register(PostAssertion, PostAssertionAdmin)


class PostNoteInline(admin.StackedInline):
    model = Post.notes.through

    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)

    extra = 0

    verbose_name = 'Post Note'
    verbose_name_plural = 'Post Notes'
    raw_id_fields = ('postnote', )

    readonly_fields = ('id', )


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'note_type', 'secondary_source', 'text', 'extra_info', 'created', 'modified')
    list_display_links = ('note_type', 'secondary_source', 'text', 'extra_info')
    readonly_fields = ('id', 'created', 'modified')

    search_fields = ['id', 'note_type', 'text']
    fields = ('id', ['secondary_source', 'note_type'], 'text', 'extra_info', )

    show_change_link = True


admin.site.register(PostAssertionNote, NoteAdmin)
admin.site.register(PostNote, NoteAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location_type', 'created', 'modified')
    list_display_links = ('id', 'name', 'location_type', )
    readonly_fields = ('id', 'created', 'modified')

    search_fields = ['id', 'name', ]
    fields = ('id', ['name', 'location_type'], 'description' )

    show_change_link = True

admin.site.register(Location, LocationAdmin)


class PersonInline(admin.StackedInline):
    model = PostAssertion
    form = PostInlineForm

    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)

    verbose_name_plural = 'Persons on this Post'
    verbose_name = 'Person:'

    show_change_link = True

    fields = (
        ['id', 'review_flag', 'position'] ,
        ['person',],
        ['role', 'uncertain'],
        ['secondary_source', 'original_text', 'office_xref'],
        ['date_display_text', ],
        ['date_source_text', 'date_secondary_source', ],
        ['date_start', 'date_start_uncertain', 'date_end', 'date_end_uncertain'],
        'notes',
        'edit_link'
    )

    sortable_field_name = 'position'

    readonly_fields = ('id', )

    raw_id_fields = ('person', 'notes')
    related_lookup_fields = {
        'fk': ['person', ],
        'm2m': ['notes', ]
    }

    extra = 0


class PostAssertionInline(admin.StackedInline):
    model = PostAssertion
    form = PostInlineForm

    extra = 0

    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)

    verbose_name = 'Post'
    verbose_name_plural = 'Person Posts'

    show_change_link = True

    ordering = ('-date_start', '-date_end', )

    readonly_fields = ('id', )

    fields = (['id', 'review_flag', ] ,
            ['post',],
            ['role', 'uncertain'],
            ['secondary_source', ],
            ['original_text', 'office_xref'],
            'date_display_text',
            ['date_source_text', 'date_secondary_source', ],
            ['date_start', 'date_start_uncertain', 'date_end', 'date_end_uncertain'],
            'notes',
            'edit_link',
            )

    raw_id_fields = ('notes', 'post', )

    related_lookup_fields = {
        'fk': ['post', ],
        'm2m': ['notes', ],
    }


class REUpdatedListFilter(SimpleListFilter):
    title = 'RE Updated'
    parameter_name = 're_updated'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(re_number_old__exact='')

        if self.value() == 'no':
            return queryset.filter(re_number_old__exact='')


class PostYearListFilter(SimpleListFilter):
    title = 'post year'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        lookup = []
        years = Post.objects.all().values('date_year').distinct()

        for year in years:
            item = (year['date_year'], year['date_year'])
            if item not in lookup:
                lookup.append(item)

        return sorted(lookup)


    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(date__year__exact=self.value())


class PersonAdmin(admin.ModelAdmin):

    fieldsets = [
            ('Database',
                 {'fields': [('id', 'review_flag')]},),
            ('General Info',
                {
                'classes': ('grp-collapse grp-open',),
                'fields': [
                    ('sex',),
                    ('praenomen', 'praenomen_uncertain'),
                    ('nomen', 'nomen_uncertain'),
                    ('filiation', 'filiation_uncertain'),
                    ('cognomen', 'cognomen_uncertain'),
                    ('other_names', ),
                    ('gens', 'gens_uncertain',),
                    ('tribe', 'tribe_uncertain'),
                    ('origin', ),
                ]}),
            ('RE',
                {'classes': ('grp-collapse grp-open',),
                'fields': [
                    ('re_number', 're_number_old', ),
                ]}
            ),
        ('Dates', {
            'classes': ('grp-collapse grp-open',),
            'fields': [
                ('date_display_text'),
                ('date_source_text', 'date_secondary_source'),
                ('date_first', 'date_first_type'),
                ('date_last', 'date_last_type'),
                ('era_from', 'era_to'),
        ]}),
        ('Patrician', {
            'classes': ('grp-collapse grp-open',),
            'fields': [('patrician', 'patrician_uncertain'),
                              ('patrician_notes')]}),
        ('Novus', {
            'classes': ('grp-collapse grp-open',),
            'fields': [('novus', 'novus_uncertain'),
                              ('novus_notes')]}),
        ('Nobilis', {
            'classes': ('grp-collapse grp-open',),
            'fields': [('nobilis', 'nobilis_uncertain'),
                                ('novus_notes')]}),
        ('Eques', {
            'classes': ('grp-collapse grp-open',),
            'fields': [('eques', 'eques_uncertain'),
                              ('eques_notes')]}),
        ]

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

    search_fields = ['id', 'nomen', 'cognomen', 'praenomen__abbrev',
                    'praenomen__name', 'other_names', 're_number', ]

    list_filter = ('postassertion__role', 'nomen', 'postassertion__post__office',
                   'review_flag', REUpdatedListFilter, 'patrician', 'novus',
                   'nobilis', 'eques', )

    inlines = (PostAssertionInline, )
    exclude = ('assertions', )

admin.site.register(Person, PersonAdmin)


class PostInline(admin.TabularInline):
    model = Post
    classes = ('grp-collapse grp-open',)

    readonly_fields = ('id', 'get_persons', 'related_label')
    fields = ('id', 'related_label', 'get_persons')
    extra = 0


class OfficeAdmin(DjangoMpttAdmin):
    readonly_fields = ('id', )
    mptt_indent_field = "name"

    list_display = (
        'id',
        'name',
        'description',
        )

    inlines = (PostInline, )

admin.site.register(Office, OfficeAdmin)


class PostAdmin(admin.ModelAdmin):

    search_fields = ['id', 'postassertion__person__nomen', 'postassertion__person__cognomen', ]
    list_filter = (PostYearListFilter, 'office')

    list_display = (
        'id',
        'office',
        'date_year',
        'date_info',
        'location',
        'uncertain',
        'modified',
        'created',
    )

    readonly_fields = ('id', )
    list_display_links = ('id', 'uncertain', 'office', )

    raw_id_fields = ('office', 'location')
    autocomplete_lookup_fields = {
        'fk': ['office', 'location', ],
    }

    fieldsets = [ ('Database Info', {'fields': ['id']}),
                    ('Post',
                        {
                        'fields': [
                                ( 'office', 'uncertain', ),
                                ('date_year', 'date_info', ),
                                ('location', )
                                ],
                        }
                    ),
            ]

    inlines = [PersonInline, PostNoteInline, ]
    exclude = ('persons',  )

admin.site.register(Post, PostAdmin)


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


