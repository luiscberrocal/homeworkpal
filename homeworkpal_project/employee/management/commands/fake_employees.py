from django.core.management import BaseCommand
from employee.models import CompanyGroup
from employee.tests.factories import CompanyGroupEmployeeAssignmentFactory, PositionAssignmentFactory, \
    CompanyGroupFactory

__author__ = 'luiscberrocal'

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('quantity')

    def handle(self, *args, **options):
        group, created = CompanyGroup.objects.get_or_create(name='TINO-NS')
        for i in range(1, int(options['quantity'])):
            group_assignment = CompanyGroupEmployeeAssignmentFactory.create(group=group)
            position_assignment = PositionAssignmentFactory.create(employee=group_assignment.employee)
            self.stdout.write('Employee %s (%s) at position %s' %(group_assignment.employee, group, position_assignment.position ))

