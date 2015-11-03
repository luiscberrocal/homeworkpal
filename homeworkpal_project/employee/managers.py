from django.db.models import Manager


__author__ = 'lberrocal'





class CompanyGroupEmployeeAssignmentManager(Manager):

    def group_members(self, company_group):
        return self.get_queryset().filter(group=company_group, end_date__isnull=True).select_related('employee', 'employee__user')


class EmployeeManager(Manager):

    def get_queryset(self):
        queryset = super(EmployeeManager, self).get_queryset().filter(user__is_active=True).select_related('user')
        return queryset

    def from_group(self, company_group):
        from employee.models import CompanyGroupEmployeeAssignment
        if isinstance(company_group, str):
            group_assignemnts = CompanyGroupEmployeeAssignment.objects.filter(group__slug=company_group).select_related('employee', 'employee__user')
        else:
            group_assignemnts = CompanyGroupEmployeeAssignment.objects.filter(group=company_group).select_related('employee', 'employee__user')
        employees_pk = list()
        for group in group_assignemnts:
            employees_pk.append(group.employee)
            #employees_pk.append(group.employee.pk)
        #return self.get_queryset().filter(pk__in=employees_pk).select_related('user')
        return employees_pk