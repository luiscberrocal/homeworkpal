from django.contrib import admin

# Register your models here.
from .models import Project, ProjectGoal, Stakeholder, Deliverable, CorporateGoalAssignment, CorporateGoal, \
    Risk, ProjectMember


class ProjectMemberInLine(admin.TabularInline):
    model = ProjectMember
    extra = 1

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
    list_display = [ 'name', 'fiscal_year', 'number', 'description']

class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ['project','employee', 'role', 'start_date', 'end_date']
    list_editable = ['employee', 'role', 'start_date', 'end_date']

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'priority', 'group', 'type', 'planned_start_date', 'planned_end_date', 'planned_man_hours' , 'actual_start_date', 'actual_end_date']
    list_editable = ['priority', 'planned_start_date', 'planned_end_date', 'planned_man_hours', 'actual_start_date', 'actual_end_date' ]
    inlines = [DeliverableInLine, StakeholderInLine, CorporateGoalAssignmentInLine, RiskInLine, ProjectMemberInLine]


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


class CorporateGoalAssignmentAdmin(admin.ModelAdmin):
    list_display = ['corporate_goal', 'project']

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectGoal, ProjectGoalAdmin)
admin.site.register(Stakeholder, StakeholderAdmin)
admin.site.register(Deliverable, DeliverableAdmin)
admin.site.register(CorporateGoal, CorporateGoalAdmin)
admin.site.register(Risk, RiskAdmin)
admin.site.register(ProjectMember, ProjectMemberAdmin)
admin.site.register(CorporateGoalAssignment, CorporateGoalAssignmentAdmin)