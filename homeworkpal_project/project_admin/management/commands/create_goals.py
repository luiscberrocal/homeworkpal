from datetime import date
from django.core.management import BaseCommand
from common.utils import get_fiscal_year
from project_admin.models import ProjectMember, ProjectGoal, IndividualGoal
import logging
logger = logging.getLogger(__name__)
__author__ = 'lberrocal'

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('fiscal_year', nargs='?')


    def handle(self, *args, **options):
        default_fiscal_year = get_fiscal_year(date.today())
        #logger.debug('Default FY %s' % default_fiscal_year)
        if options['fiscal_year'] is None:
            fiscal_year = default_fiscal_year
        else:
            fiscal_year = options['fiscal_year']
        self.stdout.write('Creating goals for fiscal year %s' % fiscal_year)
        members = ProjectMember.objects.filter(project__fiscal_year=fiscal_year).select_related('project', 'employee')
        created_count = 0
        updated_count = 0
        count = 0
        for member in members:
            default_data = {'weight' : 0.1}
            goal, created = IndividualGoal.objects.get_or_create(project=member.project,
                                                              employee=member.employee,
                                                              fiscal_year=fiscal_year,
                                                              defaults=default_data)
            count += 1
            if created:
                action = 'Created'
                created_count += 1
            else:
                goal.update_goal_info = True
                goal.save()
                action = 'Updated'
                updated_count += 1
            self.stdout.write('%d %s Goal %s for %s' % (count, action, goal.name, goal.employee))
        self.stdout.write('Created %d Updated %d Total %d' % (created_count, updated_count, count))







