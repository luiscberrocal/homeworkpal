import re

from django.db.models import Manager


__author__ = 'lberrocal'


class EmployeeManager(Manager):

    def get_queryset(self):
        queryset = super(EmployeeManager, self).get_queryset().filter(user__is_active=True).select_related('user')
        return queryset

    def _is_slug(self, company_group):
        regexp = r'^[a-z0-9-]*$'
        pattern = re.compile(regexp)
        if pattern.match(company_group):
            return True
        else:
            return False

    def from_group(self, company_group):
        from .models import CompanyGroupEmployeeAssignment
        if isinstance(company_group, str):
            if self._is_slug(company_group):
                group_assignemnts = CompanyGroupEmployeeAssignment.objects.filter(group__slug=company_group).select_related('employee', 'employee__user')
            else:
                group_assignemnts = CompanyGroupEmployeeAssignment.objects.filter(group__name=company_group).select_related('employee', 'employee__user')
        else:
            group_assignemnts = CompanyGroupEmployeeAssignment.objects.filter(group=company_group).select_related('employee', 'employee__user')
        employees_pk = list()
        for group in group_assignemnts:
            employees_pk.append(group.employee.pk)
        return self.get_queryset().filter(pk__in=employees_pk).select_related('user')



class CompanyGroupEmployeeAssignmentManager(Manager):

    def group_members(self, company_group):
        return self.get_queryset().filter(group=company_group, end_date__isnull=True).select_related('employee', 'employee__user')