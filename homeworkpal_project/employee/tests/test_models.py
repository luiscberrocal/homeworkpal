
import logging
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from employee.models import Employee, Position, CompanyGroupEmployeeAssignment
from employee.tests.factories import UserFactory, EmployeeFactory, PositionFactory, \
    CompanyGroupEmployeeAssignmentFactory, CompanyGroupFactory

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

    def test_get_current_group(self):
        group_assignment = CompanyGroupEmployeeAssignmentFactory.create()
        employee = group_assignment.employee
        logger.debug('Employee: %s Group: %s started: %s' % (group_assignment.employee,
                                                             group_assignment.group,
                                                             group_assignment.start_date.strftime('%Y-%m-%d')))
        self.assertEqual(employee.group.id, group_assignment.group.id)

    def test_no_current_group(self):
        employee = EmployeeFactory.create()
        self.assertIsNone(employee.group)




class TestPositions(TestCase):

    def test_create(self):
        position = PositionFactory.create()
        logger.debug(position)
        self.assertEqual(Position.objects.all().count(), 1)


class TestCompanyGroupEmployeeAssignment(TestCase):

    def test_create(self):
        group_assignment = CompanyGroupEmployeeAssignmentFactory.create()
        logger.debug('Employee: %s Group: %s started: %s' % (group_assignment.employee,
                                                             group_assignment.group,
                                                             group_assignment.start_date.strftime('%Y-%m-%d')))
        self.assertEqual(CompanyGroupEmployeeAssignment.objects.all().count(), 1)

    def test_previous_assingment(self):
        group_assignment = CompanyGroupEmployeeAssignmentFactory.create()
        logger.debug('Employee: %s Group: %s started: %s' % (group_assignment.employee,
                                                             group_assignment.group,
                                                             group_assignment.start_date.strftime('%Y-%m-%d')))
        new_start_date = group_assignment.start_date + timedelta(days=90)
        new_group_assingment = CompanyGroupEmployeeAssignmentFactory.build(employee=group_assignment.employee,
                                                                           start_date=new_start_date)
        logger.debug('New assingment Employee: %s Group: %s started: %s' % (new_group_assingment.employee,
                                                             new_group_assingment.group,
                                                             new_group_assingment.start_date.strftime('%Y-%m-%d')))
        try:
            new_group_assingment.save()
            self.fail()
        except ValidationError:
            pass

class TestCompanyGroup(TestCase):

    def test_assign(self):
        assignment = CompanyGroupEmployeeAssignmentFactory.create()
        group = CompanyGroupFactory.create()
        start_date = assignment.start_date + timedelta(days=90)
        group.assign(employee=assignment.employee, start_date=start_date)
        employee = Employee.objects.get(pk=assignment.employee.id)
        self.assertEqual(group.id, employee.group.id)

        assingments = CompanyGroupEmployeeAssignment.objects.filter(employee__exact=employee)
        for assign in assingments:
            logger.debug('Employee: %s Group: %s started: %s' % (assign.employee,
                                                             assign.group,
                                                             assign.start_date.strftime('%Y-%m-%d')))
        self.assertEqual(2, len(assingments))

