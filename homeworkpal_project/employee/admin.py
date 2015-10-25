from django.contrib import admin

# Register your models here.
from employee.models import Employee, CompanyGroup, CompanyGroupEmployeeAssignment


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_id', 'tenure']


class CompanyGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


class CompanyGroupEmployeeAssignmentAdmin(admin.ModelAdmin):
    list_display = ['group', 'employee', 'start_date', 'end_date']
    ordering = ['group', 'employee']

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(CompanyGroup, CompanyGroupAdmin)
admin.site.register(CompanyGroupEmployeeAssignment, CompanyGroupEmployeeAssignmentAdmin)

