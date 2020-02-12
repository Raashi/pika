from django.contrib import admin

from .models import Keyword, Job, Company, Genre


admin.site.register(Keyword)
admin.site.register(Job)
admin.site.register(Company)
admin.site.register(Genre)
