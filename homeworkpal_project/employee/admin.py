from django.contrib import admin

# Register your models here.
from employee.models import Employee, CompanyGroup, CompanyGroupEmployeeAssignment, Position, PositionAssignment


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_id', 'tenure']


class CompanyGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


class CompanyGroupEmployeeAssignmentAdmin(admin.ModelAdmin):
    list_display = ['group', 'employee', 'start_date', 'end_date']
    ordering = ['group', 'employee']


class PositionAdmin(admin.ModelAdmin):
    list_display = ('number', 'grade', 'type', 'owner')
    list_editable = ('owner',)


class PositionAssignmentAdmin(admin.ModelAdmin):
    list_display = ['position', 'employee', 'start_date', 'end_date']
    list_editable = ['employee', 'start_date', 'end_date']

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(CompanyGroup, CompanyGroupAdmin)
admin.site.register(CompanyGroupEmployeeAssignment, CompanyGroupEmployeeAssignmentAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(PositionAssignment, PositionAssignmentAdmin)