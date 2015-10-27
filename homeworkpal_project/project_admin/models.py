from autoslug import AutoSlugField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from employee.models import Employee, CompanyGroup


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
    slug = AutoSlugField(populate_from='short_name', max_length=60, unique=True)
    planned_man_hours = models.DecimalField(max_digits=7, decimal_places=2)
    type = models.CharField(max_length=8, choices=PROJECT_TYPES, default=MAIN_PROJECT)
    group = models.ForeignKey(CompanyGroup, null=True)
    priority = models.IntegerField(default=10, help_text='The lower the number the higher the priority')

    class Meta:
        ordering = ['priority', 'planned_man_hours']

    def __str__(self):
        return self.short_name

class Deliverable(models.Model):
    project = models.ForeignKey(Project, related_name='deliverables')
    name = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return '%s - %s' %(self.project, self.name)

class ProjectGoal(models.Model):
    project = models.ForeignKey(Project)
    employee = models.ForeignKey(Employee)
    weight = models.FloatField(validators=[MaxValueValidator(1.0), MinValueValidator(0.0)])
    expected_advancement = models.FloatField(validators=[MaxValueValidator(1.0), MinValueValidator(0.0)], default=0.9)


class Stakeholder(models.Model):
    employee = models.ForeignKey(Employee, related_name='projects_as_stakeholder')
    project = models.ForeignKey(Project, related_name='stakeholders')
    rank = models.IntegerField(default=10, help_text='Rank of the stakeholder in the project')

    class Meta:
        ordering = ['project', 'rank']
