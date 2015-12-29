from django.core.management import BaseCommand
from employee.models import CompanyGroup
from employee.tests.factories import CompanyGroupEmployeeAssignmentFactory, PositionAssignmentFactory, \
    CompanyGroupFactory
from maximo.tests.factories import MaximoTicketFactory

__author__ = 'luiscberrocal'

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--tickets',
            action='store_true',
            dest='tickets',
            default=False,
            help='Creates maximo tickets')
        parser.add_argument('--ticket-type',
            action='store',
            dest='ticket_type',
            default='SR',
            help='Ticket type to create')
        parser.add_argument('quantity')

    def handle(self, *args, **options):
        if options['tickets']:
            for i in range(1, int(options['quantity'])+1):
                ticket = MaximoTicketFactory.create(ticket_type=options['ticket_type'])
                self.stdout.write('%d Ticket %s (%s)' %(i, ticket.number, ticket.ticket_type))

