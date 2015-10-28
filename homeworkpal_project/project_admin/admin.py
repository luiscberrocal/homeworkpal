from django.contrib import admin

# Register your models here.
from project_admin.models import Project, ProjectGoal, Stakeholder, Deliverable, CorporateGoalAssignment, CorporateGoal, \
    Risk


class DeliverableInLine(admin.TabularInline):
    model = Deliverable
    extra = 1


class StakeholderInLine(admin.TabularInline):
    model = Stakeholder
    extra = 1


class CorporateGoalAssignmentInLine(admin.TabularInline):
    model = CorporateGoalAssignment
    extra = 1

class RiskInLine(admin.TabularInline):
    model = Risk
    extra = 1

class CorporateGoalAdmin(admin.ModelAdmin):
    model = CorporateGoal
    list_display = [ 'fiscal_year', 'number', 'description']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'priority', 'group', 'type', 'planned_start_date', 'planned_end_date', 'planned_man_hours']
    list_editable = ['priority', 'planned_start_date', 'planned_end_date', 'planned_man_hours' ]
    inlines = [DeliverableInLine, StakeholderInLine, CorporateGoalAssignmentInLine, RiskInLine]


class ProjectGoalAdmin(admin.ModelAdmin):
    list_display = ['project', 'employee', 'weight', 'expected_advancement']
    list_editable = ['weight']
    ordering = ['employee', 'project']
    list_filter = ('employee',)


class StakeholderAdmin(admin.ModelAdmin):
    list_display = ['project', 'employee', 'rank']


class DeliverableAdmin(admin.ModelAdmin):
    list_display = ['project', 'name']

class RiskAdmin(admin.ModelAdmin):
    list_display = ['risk_type', 'project', 'priority', 'description']

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectGoal, ProjectGoalAdmin)
admin.site.register(Stakeholder, StakeholderAdmin)
admin.site.register(Deliverable, DeliverableAdmin)
admin.site.register(CorporateGoal, CorporateGoalAdmin)
admin.site.register(Risk, RiskAdmin)