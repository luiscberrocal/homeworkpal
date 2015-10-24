import logging
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from employee.models import Employee, Position, CompanyGroupEmployeeAssignment
from employee.tests.factories import UserFactory, EmployeeFactory, PositionFactory, \
    CompanyGroupEmployeeAssignmentFactory

__author__ = 'luiscberrocal'

logger = logging.getLogger(__name__)

class TestUsers(TestCase):

    def test_create_user(self):
        #settings.configure()
        user = UserFactory.create()
        logger.debug(user)
        self.assertEqual(User.objects.all().count(),1)

class TestEmployees(TestCase):

    def test_create(self):
        employee = EmployeeFactory.create()
        logger.debug(employee)
        self.assertEqual(Employee.objects.all().count(), 1)

class TestPositions(TestCase):

    def test_create(self):
        position = PositionFactory.create()
        logger.debug(position)
        self.assertEqual(Position.objects.all().count(), 1)


class TestCompanyGroupEmployeeAssignment(TestCase):

    def test_create(self):
        group_assignemt = CompanyGroupEmployeeAssignmentFactory.create()
        logger.debug('Employee: %s Group: %s started: %s' % (group_assignemt.employee,
                                                             group_assignemt.group,
                                                             group_assignemt.start_date.strftime('%Y-%m-%d')))
        self.assertEqual(CompanyGroupEmployeeAssignment.objects.all().count(), 1)