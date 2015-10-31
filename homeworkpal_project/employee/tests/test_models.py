
import logging
from datetime import timedelta, datetime, date
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import Employee, Position, CompanyGroupEmployeeAssignment
from .factories import UserFactory, EmployeeFactory, PositionFactory, \
    CompanyGroupEmployeeAssignmentFactory, CompanyGroupFactory, PositionAssignmentFactory

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

    def test_no_current_position(self):
        employee = EmployeeFactory.create()
        self.assertIsNone(employee.position)

    def test_get_current_position(self):
        position_assignment = PositionAssignmentFactory.create()
        self.assertEqual(position_assignment.employee.position, position_assignment.position)




class TestPositions(TestCase):

    def test_create(self):
        position = PositionFactory.create()
        logger.debug(position)
        self.assertEqual(Position.objects.all().count(), 1)

    def test_assign_2_postions(self):
        position = PositionFactory.create()
        position_assignment = PositionAssignmentFactory.create()
        start_date = position_assignment.start_date + timedelta(days=90)
        position.assign(employee=position_assignment.employee, start_date=start_date)
        employee = Employee.objects.get(pk=position_assignment.employee.pk)
        self.assertEqual(employee.position, position)



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

    def test_group_members(self):
        group_assignment = CompanyGroupEmployeeAssignmentFactory.create()
        group_assignment.end_date = date.today()
        group_assignment.save()
        employees = EmployeeFactory.create_batch(5)
        for employee in employees[:3]:
            logger.debug('****')
            group_assignment.group.assign(employee, date.today())
        members = CompanyGroupEmployeeAssignment.objects.group_members(group_assignment.group)
        self.assertEqual(3, len(members))


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


class TestPositionAssignment(TestCase):

    def test_create_2_active_positions(self):
        position_assignment = PositionAssignmentFactory.create()
        position = PositionFactory.create()
        start_date = position_assignment.start_date + timedelta(days=90)
        try:
            PositionAssignmentFactory.create(employee=position_assignment.employee,
                                             position=position,
                                             start_date=start_date)
            self.fail('Allowed the creation of duplicate current positions')
        except ValidationError:
            pass

