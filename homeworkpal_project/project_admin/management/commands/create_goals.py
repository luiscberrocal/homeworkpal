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
        parser.add_argument('--create-goals',
                            action='store_true',
                            dest='create_goals',
                            default=None,
                            help='Create goals based on project membership')
        parser.add_argument('--assign-goal',
                            action='store_true',
                            dest='assign_goal',
                            default=None,
                            help='Assign specific goals to a company group')
        parser.add_argument('--goal-pk',
                            action='store',
                            dest='goal_pk',
                            default=None,
                            help='Primary key of goal')
        parser.add_argument('--group',
                            action='store',
                            dest='companygroup_name',
                            default=None,
                            help='Company group slug')

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
            count = 0
            created_count = 0
            for employee in employees:
                goal_pk, created = goal.copy(employee)
                count += 1
                if created:
                    created_count += 1
                    action = 'Created'
                    self.stdout.write('%d Copied %s goal to employee %s' % (count, goal, employee))
                else:
                    self.stdout.write('%d Already assigned goal %s to %s' % (count, goal, employee))

        except IndividualGoal.DoesNotExist:
             self.stderr.write('There is no goal with primary key %d' % goal_pk)



    def handle(self, *args, **options):
        '''
        python manage.py create_goals --assign-goal --goal-pk=43 --group=tino-ns
        :param args:
        :param options:
        :return:
        '''
        default_fiscal_year = get_fiscal_year(date.today())
        #logger.debug('Default FY %s' % default_fiscal_year)
        if options['fiscal_year'] is None:
            fiscal_year = default_fiscal_year
        else:
            fiscal_year = options['fiscal_year']
        if options['create_goals']:
            self._create_goals_from_project_membership(fiscal_year)
        elif options['assign_goal']:
            goal_pk =int(options['goal_pk'])
            companygroup_name = options['companygroup_name']
            self._assign_goal_to_group(goal_pk, companygroup_name)









