from django.db.models import Manager

__author__ = 'lberrocal'


class CompanyGroupEmployeeAssignmentManager(Manager):

    def group_members(self, company_group):
        return self.get_queryset().filter(group=company_group, end_date__isnull=True).select_related('employee', 'employee__user')