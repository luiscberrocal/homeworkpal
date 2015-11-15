from datetime import date
from django.test import TestCase
from employee.models import Employee
from maximo.models import MaximoTicket, MaximoTimeRegister
from maximo.tests.factories import MaximoTicketFactory, MaximoTimeRegisterFactory
import logging
from maximo.tests.test_excel import TestExcel
from project_admin.tests.factories import ProjectFactory

__author__ = 'lberrocal'

logger = logging.getLogger(__name__)


class TestMaximoTicket(TestCase):

    def test_create(self):
        ticket = MaximoTicketFactory.create()
        self.assertEqual(6, len(ticket.number))
        self.assertEqual(1, MaximoTicket.objects.count())

    def test_batch_create(self):
        MaximoTicketFactory.create_batch(8, ticket_type='SR')
        MaximoTicketFactory.create_batch(2, ticket_type='WO')
        self.assertEqual(8, MaximoTicket.objects.filter(ticket_type='SR').count())
        self.assertEqual(2, MaximoTicket.objects.filter(ticket_type='WO').count())


class TestMaximoTimeRegister(TestCase):

    fixtures = ['employee_fixtures.json', 'maximo_ticket_fixtures.json']

    def test_fixtures_loaded(self):
        self.assertEqual(14, Employee.objects.count())

    def test_create(self):
        register = MaximoTimeRegisterFactory.create()
        self.assertEqual(1, MaximoTimeRegister.objects.count())

    def test_get_employee_total_regular_hours(self):
        register = MaximoTimeRegisterFactory.create()
        register2 = MaximoTimeRegisterFactory.create(employee=register.employee, date=register.date, pay_rate=register.pay_rate)
        registers = MaximoTimeRegister.objects.get_employee_total_regular_hours(employee=register.employee, date=register.date)
        self.assertEqual(2, len(registers))
        self.assertEqual(16, registers['total_regular_hours'])
        self.assertEqual(2, registers['register_count'])

    def test_get_employee_total_regular_hours_no_data(self):
        employee = Employee.objects.all()[:1][0]
        registers = MaximoTimeRegister.objects.get_employee_total_regular_hours(employee=employee, date=date.today())
        self.assertIsNone(registers['total_regular_hours'])
        self.assertEquals(0, registers['register_count'])

    def test_get_or_create(self):
        data = dict()
        data['employee'] = Employee.objects.all()[:1][0]
        data['ticket'] = MaximoTicket.objects.all()[:1][0]
        data['date'] = date(2015, 10, 1)
        data['regular_hours'] = 4
        data['pay_rate'] = 21.08

        register, created = MaximoTimeRegister.objects.get_or_create(**data)
        self.assertTrue(created)
        self.assertTrue(data['employee'], register.employee)
        register2, created = MaximoTimeRegister.objects.get_or_create(**data)
        self.assertFalse(created)
        self.assertEquals(register.pk, register2.pk)

    def test_assign_projects_from_ticket(self):
        project = ProjectFactory.create()
        tickets = MaximoTicket.objects.all()[:5]
        for ticket in tickets:
            ticket.project = project
            ticket.save()
        TestExcel.create_time_registers(date(2015, 9, 1), date(2015, 9, 30))
        updated = MaximoTimeRegister.objects.assign_projects_from_ticket()
        self.assertEqual(294, updated)
        registers = MaximoTimeRegister.objects.filter(project__isnull=False)
        self.assertEqual(149, len(registers))

    # def test_assign_projects_from_ticket_filter(self):
    #     project = ProjectFactory.create()
    #     tickets = MaximoTicket.objects.all()[:5]
    #     for ticket in tickets:
    #         ticket.project = project
    #         ticket.save()
    #     TestExcel.create_time_registers(date(2015, 9, 1), date(2015, 9, 30))
    #     updated = MaximoTimeRegister.objects.filter(date__range=(date(2015, 9, 1), date(2015, 9, 15))).assign_projects_from_ticket()
    #     self.assertEqual(0, updated)
    #     registers = MaximoTimeRegister.objects.filter(project__isnull=False)
    #     self.assertEqual(0, len(registers))



