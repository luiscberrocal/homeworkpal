from django.contrib import admin

# Register your models here.
from .models import StashProject, StashRepository


class StashProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class StashRepositoryAdmin(admin.ModelAdmin):
    list_display = ('software_name', 'project', 'name', 'description')


admin.site.register(StashProject, StashProjectAdmin)
admin.site.register(StashRepository, StashRepositoryAdmin)
