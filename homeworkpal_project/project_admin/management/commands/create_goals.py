from django.core.management import BaseCommand
from project_admin.models import ProjectMember, ProjectGoal

__author__ = 'lberrocal'

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('fiscal_year', nargs='?')


    def handle(self, *args, **options):
        fiscal_year = options.get('fiscal_year', 'AF16')
        members = ProjectMember.objects.filter(project__fiscal_year=fiscal_year).select_related('project', 'employee')
        created_count = 0
        updated_count = 0
        count = 0
        for member in members:
            goal, created = ProjectGoal.objects.get_or_create(project=member.project,
                                                              employee=member.employee,
                                                              fiscal_year=fiscal_year)
            count += 1
            if created:
                action='Created'
                created_count += 1
            else:
                action='Updated'
                updated_count += 1
            self.stdout.write('%d %s Goal %s for %s' % (count, goal.name, goal.employee))
        self.stdout.write('Created %d Updated %d Total %d' (created_count, updated_count, count))







