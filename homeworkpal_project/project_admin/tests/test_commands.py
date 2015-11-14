from datetime import date
from django.core.management import call_command
from django.test import TestCase
from employee.tests.factories import CompanyGroupFactory, EmployeeFactory
from project_admin.models import IndividualGoal
from project_admin.tests.factories import IndividualGoalFactory

__author__ = 'lberrocal'


class TestProjectAdminCommand(TestCase):

    def test_create_goals(self):
        company_group = CompanyGroupFactory.create(name='TINO-NS')
        employees = EmployeeFactory.create_batch(10)
        goal = IndividualGoalFactory.create()
        self.assertEqual(1, IndividualGoal.objects.count())
        for employee in employees:
            company_group.assign(employee, date.today())
        call_command('create_goals', assign_goal=True, goal_pk=goal.pk, companygroup_name=company_group.slug)
        self.assertEqual(11, IndividualGoal.objects.count())


