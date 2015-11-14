from django.test import TestCase
from employee.tests.factories import EmployeeFactory
from ..models import ProjectMember, ProjectGoal
from .factories import ProjectMemberFactory, ProjectGoalFactory, ProjectFactory

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


    def test_retrieve_project_member(self):
        member = ProjectMemberFactory.create()
        db_member = ProjectMember.objects.get(project=member.project, employee=member.employee)
        self.assertEqual(member.pk, db_member.pk)


class TestProjectGoal(TestCase):

    def test_create(self):
        goal = ProjectGoalFactory.create()
        self.assertEqual(1, ProjectGoal.objects.count())
        self.assertIsNone(goal.project)

    def test_create_with_project(self):
        member = ProjectMemberFactory.create()
        project = member.project
        goal = ProjectGoalFactory.create(project=project, employee=member.employee)
        self.assertTrue(goal.pk > 0)
        self.assertEqual(project.short_name, goal.name)
        self.assertEqual(project.description, goal.description)
        self.assertTrue(goal.expectations.startswith('Haber alcanzado el '))
        self.assertTrue(goal.fiscal_year.startswith('AF'))



