from django.test import TestCase
from employee.tests.factories import EmployeeFactory
from project_admin.models import ProjectMember
from project_admin.tests.factories import ProjectMemberFactory

import logging

logger = logging.getLogger(__name__)
__author__ = 'lberrocal'




class TestProjectMember(TestCase):

    def test_create(self):
        ProjectMemberFactory.create()
        count = ProjectMember.objects.count()
        self.assertEqual(1, count)

    def test_assigned_to_project(self):
        employees = EmployeeFactory.create_batch(10)
        member = ProjectMemberFactory.create()
        for employee in employees[:5]:
            ProjectMemberFactory.create(project=member.project, employee=employee)
        assigned = ProjectMember.objects.assigned_to_project(member.project)
        self.assertEqual(6, len(assigned))

    # def test_unassigned_to_project(self):
    #     employees = EmployeeFactory.create_batch(10)
    #     member = ProjectMemberFactory.create()
    #     for employee in employees[:5]:
    #         ProjectMemberFactory.create(project=member.project, employee=employee)
    #     self.assertEqual(6, ProjectMember.objects.count())
    #     unassigned = ProjectMember.objects.unassigned_to_project(member.project)
    #     self.assertEqual(5, len(unassigned))


