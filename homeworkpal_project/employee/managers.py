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
        from .models import CompanyGroupEmployeeAssignment, CompanyGroup
        if isinstance(company_group, str):
            try:
                if self._is_slug(company_group):
                    company_group = CompanyGroup.objects.get(slug=company_group)
                    #group_assignemnts = CompanyGroupEmployeeAssignment.objects.filter(group__slug=company_group, end_date=None).select_related('employee', 'employee__user')
                else:
                    company_group = CompanyGroup.objects.get(name=company_group)
                    #group_assignemnts = CompanyGroupEmployeeAssignment.objects.filter(group__name=company_group, end_date=None).select_related('employee', 'employee__user')
            except CompanyGroup.DoesNotExist:
                company_group = None

        group_assignments = CompanyGroupEmployeeAssignment.objects.group_members(company_group=company_group)
        employees_pk = list()
        for group in group_assignments:
            employees_pk.append(group.employee.pk)
        return self.get_queryset().filter(pk__in=employees_pk).select_related('user')


class CompanyGroupEmployeeAssignmentManager(Manager):

    def group_members(self, company_group):
        return self.get_queryset().filter(group=company_group, end_date__isnull=True).select_related('employee', 'employee__user')

    def group_leader(self, company_group):
        from .models import CompanyGroupEmployeeAssignment
        qs = self.get_queryset().filter(group=company_group, end_date__isnull=True, role=CompanyGroupEmployeeAssignment.LEADER_ROLE).select_related('employee', 'employee__user')
        if len(qs) == 0:
            return None
        elif len(qs) > 1:
            raise ValueError('Company group %s has more than one leader' % (company_group.name))
        return qs[0]