from datetime import date
from django.core.management import BaseCommand
from common.utils import get_fiscal_year
from employee.models import CompanyGroup, CompanyGroupEmployeeAssignment, Employee
from project_admin.models import ProjectMember, ProjectGoal, IndividualGoal
import logging
logger = logging.getLogger(__name__)
__author__ = 'lberrocal'

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('fiscal_year', nargs='?')

    def _create_goals_from_project_membership(self, fiscal_year):
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

    def _assign_goal_to_group(self, goal_pk, companygroup_name):
        try:
            goal = IndividualGoal.objects.get(pk=goal_pk)
            if goal.project is not None:
                self.stderr.write('Cannot assign a goal to a group that is related to a project')
                return
            employees = Employee.objects.from_group(companygroup_name)
            if len(employees) == 0:
                self.stderr.write('There are no employees in group %s' % companygroup_name)
                return
            for employee in employees:
                pass


        except IndividualGoal.DoesNotExist:
             self.stderr.write('There is no goal with primary key %d' % goal_pk)



    def handle(self, *args, **options):
        default_fiscal_year = get_fiscal_year(date.today())
        #logger.debug('Default FY %s' % default_fiscal_year)
        if options['fiscal_year'] is None:
            fiscal_year = default_fiscal_year
        else:
            fiscal_year = options['fiscal_year']
        self._create_goals_from_project_membership(fiscal_year)









