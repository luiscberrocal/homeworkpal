
from autoslug import AutoSlugField
from datetime import timedelta
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from django.utils import timezone
from employee.models import Employee, CompanyGroup
from project_admin.managers import ProjectMemberManager
from project_admin.utils import Holiday


class Project(models.Model):
    INTERNAL_PROJECT = 'INTERNAL'
    MAIN_PROJECT = 'PROJECT'
    SUPPORT_PROJECT = 'SUPPORT'
    PROJECT_TYPES = (
        (MAIN_PROJECT, 'Proyecto'),
        (INTERNAL_PROJECT, 'Interno'),
        (SUPPORT_PROJECT, 'Apoyo')
    )
    short_name = models.CharField(max_length=60)
    description = models.TextField()
    planned_start_date = models.DateField()
    planned_end_date = models.DateField()
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    slug = AutoSlugField(populate_from='short_name', max_length=60, unique=True)
    planned_man_hours = models.DecimalField(max_digits=7, decimal_places=2)
    type = models.CharField(max_length=8, choices=PROJECT_TYPES, default=MAIN_PROJECT)
    group = models.ForeignKey(CompanyGroup, null=True)
    priority = models.IntegerField(default=10, help_text=_('The lower the number the higher the priority'))
    fiscal_year = models.CharField(max_length=4,
                                   validators=[RegexValidator(regex=r'^AF\d{2}$',
                                                              message=_('Fiscal year must us format AFYY. '
                                                                        'For example AF16 for fiscal year 2016'))])

    def _leader(self):
        try:
            member = ProjectMember.objects.select_related('employee__user').get(project=self, end_date=None, role=ProjectMember.ROLE_TEAM_LEADER)
            leader = member.employee
        except ProjectMember.DoesNotExist:
            leader = None
        return leader
    leader = property(_leader)

    def remaining_days(self):
        holidays = Holiday()
        from_date = timezone.localtime(timezone.now()).date()
        day_generator = (from_date + timedelta(x + 1) for x in range((self.planned_end_date - from_date).days))
        rd = sum(1 for day in day_generator if day.weekday() < 5 and not holidays.is_holiday(day))
        return rd

    class Meta:
        ordering = ['priority', 'planned_man_hours']

    def get_absolute_url(self):
        return reverse('project:project_detail', args=[self.pk])

    def __str__(self):
        return self.short_name


class ProjectMember(models.Model):
    ROLE_TEAM_MEMBER = 'MEMBER'
    ROLE_TEAM_LEADER = 'LEADER'
    ROLE_TEAM_PRODUCT_OWNER = 'PRODUCT_OWNER'
    ROLES = (
        (ROLE_TEAM_MEMBER, 'Team Member'),
        (ROLE_TEAM_LEADER, 'Team Leader'),
        (ROLE_TEAM_PRODUCT_OWNER, 'Product Owner'),
    )
    role = models.CharField(max_length=15, choices=ROLES, default=ROLE_TEAM_MEMBER)
    employee = models.ForeignKey(Employee, related_name='projects')
    project = models.ForeignKey(Project, related_name='members')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)

    objects = ProjectMemberManager()


class Risk(models.Model):
    RISK_THREAT = 'THREAT'
    RISK_OPPORTUNITY = 'OPPORTUNITY'
    RISK_TYPES = (
        (RISK_THREAT, 'Amenaza'),
        (RISK_OPPORTUNITY, 'Oportunidad')
    )
    risk_type = models.CharField(max_length=12, choices=RISK_TYPES, default=RISK_THREAT)
    priority = models.IntegerField(default=1)
    description = models.TextField()
    project = models.ForeignKey(Project, related_name='risks')

    class Meta:
        ordering = ('priority', '-risk_type')


class CorporateGoal(models.Model):
    number = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField()
    fiscal_year = models.CharField(max_length=4,
                                   validators=[RegexValidator(regex=r'^AF\d{2}$',
                                                              message=_('Fiscal year must us format AFYY. '
                                                                        'For example AF16 for fiscal year 2016'))])


    def __str__(self):
        return '%s - %s' % (self.number, self.description)


class CorporateGoalAssignment(models.Model):
    corporate_goal = models.ForeignKey(CorporateGoal, related_name='projects')
    project = models.ForeignKey(Project, related_name='corporate_goals')


class Deliverable(models.Model):
    project = models.ForeignKey(Project, related_name='deliverables')
    name = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return '%s - %s' %(self.project, self.name)


class ProjectGoal(models.Model):
    name = models.CharField(max_length=120, null=True)
    description = models.TextField(null=True)
    expectations = models.TextField(null=True)
    project = models.ForeignKey(Project, null=True)
    employee = models.ForeignKey(Employee, related_name='goals')
    weight = models.FloatField(validators=[MaxValueValidator(1.0), MinValueValidator(0.0)])
    expected_advancement = models.FloatField(validators=[MaxValueValidator(1.0), MinValueValidator(0.0)], default=0.9)
    update_goal_info = models.BooleanField(default=True, help_text=_('Will update name, description and expectations based on the project information'))
    fiscal_year = models.CharField(max_length=4,
                                   validators=[RegexValidator(regex=r'^AF\d{2}$',
                                                              message=_('Fiscal year must use format AFYY. '
                                                                        'For example AF16 for fiscal year 2016'))])


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.project is not None and self.update_goal_info:
            try:
                member = ProjectMember.objects.get(project=self.project, employee=self.employee)
                self.update_goal_info = False
                self.name = self.project.short_name
                self.description = self.project.description
                self.expectations = 'Haber alcanzado el 90%% de avance antes del %s.' % self.project.planned_end_date.strftime('%d-%b-%Y')

                if member.role == 'LEADER':
                    self.expectations += 'Como líder del proyecto debe apoyar la gestión del supervisor dandole seguimiento ' \
                                         'a los recursos contratados y dar informes periódicos de ' \
                                         'avances, asi como comunicar oportunamente de impedimentos ' \
                                         'y problemas.'
            except ProjectMember.DoesNotExist:
                raise ValueError('Cannot assign %s to goal '
                                 'related to project %s because he is not a member' % (self.employee, self.project))


        return super(ProjectGoal, self).save(force_insert=force_insert, force_update=force_update, using=using,
             update_fields=update_fields)


class Stakeholder(models.Model):
    employee = models.ForeignKey(Employee, related_name='projects_as_stakeholder')
    project = models.ForeignKey(Project, related_name='stakeholders')
    rank = models.IntegerField(default=10, help_text='Rank of the stakeholder in the project')

    class Meta:
        ordering = ['project', 'rank']


