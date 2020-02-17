from django.contrib import admin

from .models import Person, PersonTMDBImage


class PersonImageAdmin(admin.TabularInline):
    model = PersonTMDBImage


class PersonAdmin(admin.ModelAdmin):
    inlines = [PersonImageAdmin]


admin.site.register(Person, PersonAdmin)
