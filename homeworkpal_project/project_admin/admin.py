from django.contrib import admin

# Register your models here.
from project_admin.models import Project, ProjectGoal


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'priority', 'group', 'type', 'planned_start_date', 'planned_end_date', 'planned_man_hours']
    list_editable = ['priority', 'planned_start_date', 'planned_end_date', 'planned_man_hours' ]


class ProjectGoalAdmin(admin.ModelAdmin):
    list_display = ['project', 'employee', 'weight', 'expected_advancement']
    list_editable = ['weight']
    ordering = ['employee', 'project']
    list_filter = ('employee',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectGoal, ProjectGoalAdmin)