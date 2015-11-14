from django.db.models import Manager
from employee.models import CompanyGroupEmployeeAssignment

__author__ = 'lberrocal'



class ProjectMemberManager(Manager):

    def assigned_to_project(self, project):
        return self.get_queryset().filter(project=project).select_related('employee', 'employee__user')


    # def unassigned_to_project(self, project, company_group=None):
    #     if company_group:
    #         group_assignments = CompanyGroupEmployeeAssignment.objects.group_members(company_group)
    #         pks = self._get_employees_pk_list(group_assignments)
    #         return self.get_queryset().filter(employee__pk__in=pks).exclude(project=project,).select_related('employee', 'employee__user')
    #     else:
    #         return self.get_queryset().exclude(project=project,).select_related('employee', 'employee__user')


    def _get_employees_pk_list(self, group_assignments):
        pks = list()
        for group_assignment in group_assignments:
            pks.append(group_assignment.employee.pk)

        return pks

