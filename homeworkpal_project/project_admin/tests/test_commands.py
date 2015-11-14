from datetime import date
from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from employee.tests.factories import CompanyGroupFactory, EmployeeFactory
from project_admin.models import IndividualGoal
from project_admin.tests.factories import IndividualGoalFactory, ProjectMemberFactory

__author__ = 'lberrocal'


class TestProjectAdminCommand(TestCase):

    def test_assign_goals(self):
        out = StringIO()
        company_group = CompanyGroupFactory.create(name='TINO-NS')
        employees = EmployeeFactory.create_batch(10)
        goal = IndividualGoalFactory.create()
        self.assertEqual(1, IndividualGoal.objects.count())
        for employee in employees:
            company_group.assign(employee, date.today())
        call_command('create_goals', assign_goal=True, goal_pk=goal.pk,
                     companygroup_name=company_group.slug,
                     stdout=out)
        self.assertEqual(11, IndividualGoal.objects.count())
        self.assertTrue(out.getvalue().startswith('1 Copied '))

    def test_create_goals(self):
        out = StringIO()
        ProjectMemberFactory.create_batch(10, project__fiscal_year='AF16')
        self.assertEqual(0, IndividualGoal.objects.count())
        call_command('create_goals', 'AF16', create_goals=True, stdout=out)
        self.assertEqual(10, IndividualGoal.objects.count())
        self.assertTrue(out.getvalue().startswith('Creating goals for fiscal year AF16'))




