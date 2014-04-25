from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from models import Person, Office, Praenomen, \
    AssertionPerson, Assertion, AssertionType, RoleType, \
    Date, DateType, \
    SecondarySource

admin.site.register(AssertionType)
admin.site.register(Date)
admin.site.register(DateType)
admin.site.register(RoleType)

class AssertionPersonInline(admin.TabularInline):
    readonly_fields=('id',)
    model = AssertionPerson
    extra = 1


class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Database Info', {'fields': ['id',]}),
        ('Person',   {'fields': ['sex', 'praenomen', 'nomen', 'cognomen', 'filliation',]}),
    ]

    readonly_fields=('id',)
    list_display = ('id', 'praenomen', 'nomen', 'cognomen', 'sex', 'filliation', )

    inlines = (AssertionPersonInline,)

admin.site.register(Person, PersonAdmin)


class OfficeAdmin(MPTTModelAdmin):
    readonly_fields=('id',)
    list_display = ('id', 'name', 'parent', 'description')

admin.site.register(Office, OfficeAdmin)


class AssertionAdmin(admin.ModelAdmin):
    list_display = ('id', 'assertion_type', 'get_persons', 'display_text','secondary_source')
    list_display_links = ('id', 'display_text', )

    readonly_fields=('id',)

    inlines = [
            AssertionPersonInline,
    ]

admin.site.register(Assertion, AssertionAdmin)


class PraenomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'abbrev', 'name')
    readonly_fields=('id',)
    list_display_links = ('id', 'abbrev', 'name', )

admin.site.register(Praenomen, PraenomenAdmin)

class SecondarySourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbrev_name', 'biblio')
    readonly_fields=('id',)
    list_display_links = ('id', 'abbrev_name', 'name', 'biblio')


admin.site.register(SecondarySource, SecondarySourceAdmin)

