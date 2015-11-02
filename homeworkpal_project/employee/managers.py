from django.db.models import Manager

__author__ = 'lberrocal'


class EmployeeManager(Manager):

    def get_queryset(self):
        queryset = super(EmployeeManager, self).get_queryset().filter(user__is_active=True).select_related('user')
        return queryset

class CompanyGroupEmployeeAssignmentManager(Manager):

    def group_members(self, company_group):
        return self.get_queryset().filter(group=company_group, end_date__isnull=True).select_related('employee', 'employee__user')