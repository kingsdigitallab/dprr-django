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
    model = AssertionPerson
    extra = 1


class PersonAdmin(admin.ModelAdmin):
    inlines = (AssertionPersonInline,)

admin.site.register(Person, PersonAdmin)


class OfficeAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent', 'description')

admin.site.register(Office, OfficeAdmin)


class AssertionAdmin(admin.ModelAdmin):
    list_display = ('assertion_type', 'get_persons')

    inlines = [
            AssertionPersonInline,
    ]

admin.site.register(Assertion, AssertionAdmin)


class PraenomenAdmin(admin.ModelAdmin):
    list_display = ('abbrev', 'name')

admin.site.register(Praenomen, PraenomenAdmin)


