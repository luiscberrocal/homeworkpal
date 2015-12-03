from django.test import TestCase
from employee.tests.factories import EmployeeFactory
from ..models import ProjectMember, IndividualGoal, ProjectSupport
from .factories import ProjectMemberFactory, ProjectFactory, IndividualGoalFactory, ProjectSupportFactory
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

    def test_create_batch(self):
        member = ProjectMemberFactory.create()
        ProjectMemberFactory.create_batch(5, project=member.project)
        ProjectMemberFactory.create_batch(5)
        members = ProjectMember.objects.filter(project=member.project)
        self.assertEqual(6, len(members))
        self.assertEqual(11, ProjectMember.objects.count())


class TestIndividualGoal(TestCase):

    def test_create(self):
        goal = IndividualGoalFactory.create()
        self.assertEqual(1, IndividualGoal.objects.count())
        self.assertIsNone(goal.project)

    def test_create_with_project(self):
        member = ProjectMemberFactory.create()
        project = member.project
        goal = IndividualGoalFactory.create(project=project, employee=member.employee)
        self.assertTrue(goal.pk > 0)
        self.assertEqual(project.short_name, goal.name)
        self.assertEqual(project.description, goal.description)
        self.assertTrue(goal.expectations.startswith('Haber alcanzado el '))
        self.assertTrue(goal.fiscal_year.startswith('AF'))

    def test_copy_goal_false(self):
        goal = IndividualGoalFactory.create()
        goal_pk, created = goal.copy(goal.employee)
        self.assertFalse(created)
        self.assertTrue(goal_pk > 0)


    def test_copy_goal_true(self):
        employee = EmployeeFactory.create()
        goal = IndividualGoalFactory.create()
        goal_pk, created = goal.copy(employee)
        self.assertTrue(created)
        goal_db = IndividualGoal.objects.get(pk=goal_pk)
        self.assertIsNotNone(goal_db)


class TestProjectSupport(TestCase):

    def test_create(self):
        support = ProjectSupportFactory.create()
        self.assertEqual(1, ProjectSupport.objects.count())
        




