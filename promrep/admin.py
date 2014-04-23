from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from models import Person, Office, Assertion, AssertionPerson, Praenomen, AssertionType

admin.site.register(AssertionType)

class AssertionPersonInline(admin.TabularInline):
    model = AssertionPerson
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    inlines = (AssertionPersonInline,)

admin.site.register(Person, PersonAdmin)

class AssertionAdmin(admin.ModelAdmin):
    inlines = (AssertionPersonInline,)

admin.site.register(Assertion, AssertionAdmin)

class PraenomenAdmin(admin.ModelAdmin):
    list_display = ('abbrev', 'name')

admin.site.register(Praenomen, PraenomenAdmin)

class OfficeAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent', 'description')

admin.site.register(Office, OfficeAdmin)

