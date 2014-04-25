from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from models import Person, Office, Praenomen, \
    AssertionPerson, Assertion, AssertionType, RoleType, \
    Date, DateType, \
    SecondarySource

admin.site.register(AssertionType)
admin.site.register(Date)
admin.site.register(DateType)
admin.site.register(SecondarySource)
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

    list_display = ('id', 'assertion_type', 'get_persons', 'secondary_source')
    list_display_links = ('secondary_source', )

    readonly_fields=('id',)

    inlines = [
            AssertionPersonInline,
    ]

admin.site.register(Assertion, AssertionAdmin)


class PraenomenAdmin(admin.ModelAdmin):
    list_display = ('abbrev', 'name')
    readonly_fields=('id',)

admin.site.register(Praenomen, PraenomenAdmin)


