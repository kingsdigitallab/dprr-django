from django.contrib import admin

from models import Person, Office, Assertion, AssertionPerson, Praenomen, AssertionType

admin.site.register(Office)
admin.site.register(Praenomen)
admin.site.register(AssertionType)

class AssertionPersonInline(admin.TabularInline):
    model = AssertionPerson
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    inlines = (AssertionPersonInline,)

class AssertionAdmin(admin.ModelAdmin):
    inlines = (AssertionPersonInline,)

admin.site.register(Person, PersonAdmin)
admin.site.register(Assertion, AssertionAdmin)
