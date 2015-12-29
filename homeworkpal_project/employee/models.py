from datetime import datetime, timedelta
from autoslug import AutoSlugField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
import logging
from model_utils.models import TimeStampedModel
from .managers import CompanyGroupEmployeeAssignmentManager, EmployeeManager

logger = logging.getLogger(__name__)


# Create your models here.
PERMANENT_TYPE = 'PERM'
TEMPORARY_TYPE = 'TEMP'
TENURE_TYPES = (
    (PERMANENT_TYPE, 'Permanent'),
    (TEMPORARY_TYPE, 'Temporary')
    )


class Employee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    company_id = models.CharField(max_length=7)
    tenure = models.CharField(max_length=4, choices=TENURE_TYPES)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def _group(self):
        try:
            group_assignment = CompanyGroupEmployeeAssignment.objects.get(employee=self, end_date=None)
            group = group_assignment.group
        except CompanyGroupEmployeeAssignment.DoesNotExist:
            group = None
        return group
    group = property(_group)

    def _position(self):
        try:
            position_assingment = PositionAssignment.objects.get(employee=self, end_date=None)
            position = position_assingment.position
        except PositionAssignment.DoesNotExist:
            position = None
        return position
    position = property(_position)

    objects = EmployeeManager()

    def __str__(self):
        if self.user.last_name and self.user.first_name:
            return '%s, %s' % (self.user.last_name, self.user.first_name)
        else:
            return self.user.username


class Position(models.Model):
    number = models.CharField(max_length=6, unique=True)
    grade = models.CharField(max_length=5)
    type = models.CharField(max_length=4, choices=TENURE_TYPES)
    owner = models.OneToOneField(Employee, null=True, blank=True, related_name='permanent_position')

    def assign(self, employee, start_date):
        try:
            prev_position_assignment = PositionAssignment.objects.get(employee=employee, end_date=None)
            prev_position_assignment.end_date = start_date - timedelta(days=1)
            prev_position_assignment.save()
        except PositionAssignment.DoesNotExist:
            pass
        postion_assingment = PositionAssignment(employee=employee,
                                                position=self,
                                                start_date=start_date)
        postion_assingment.save()


    def __str__(self):
        return '%s %s' % (self.number, self.grade)


class CompanyGroup(models.Model):
    name = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=120, null=True, blank=True)
    parent_group = models.ForeignKey('self', null=True, blank=True)
    slug = AutoSlugField(populate_from='name', max_length=10, unique=True)

    def assign(self, employee, start_date):
        try:
            previous_group = CompanyGroupEmployeeAssignment.objects.get(employee=employee,
                                                                        end_date=None)
            previous_group.end_date = start_date - timedelta(days=1)
            previous_group.save()
        except CompanyGroupEmployeeAssignment.DoesNotExist:
            pass

        assignment = CompanyGroupEmployeeAssignment(employee=employee,
                                                    group=self,
                                                    start_date=start_date)
        assignment.save()

    def members(self):
        employees = list()
        assignees = CompanyGroupEmployeeAssignment.objects.group_members(self)
        for assignee in assignees:
            employees.append(assignee.employee)
        return  employees

    def __str__(self):
        return self.name


class CompanyGroupEmployeeAssignment(models.Model):
    group = models.ForeignKey(CompanyGroup)
    employee = models.ForeignKey(Employee)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    objects = CompanyGroupEmployeeAssignmentManager()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.end_date is None:
            try:
                previous_group = CompanyGroupEmployeeAssignment.objects.get(employee=self.employee,
                                                                            end_date=None)
                raise ValidationError('Employee %s is already assigned to group %s. You must'
                                       ' terminate the assingment by assingning a end date' % (previous_group.employee, previous_group.group))
            except CompanyGroupEmployeeAssignment.DoesNotExist:
                pass

        super(CompanyGroupEmployeeAssignment, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                                                     update_fields=update_fields)


class PositionAssignment(models.Model):
    position = models.ForeignKey(Position)
    employee = models.ForeignKey(Employee)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.end_date is None:
            try:
                previous_position = PositionAssignment.objects.get(employee=self.employee,
                                                                end_date=None)
                raise ValidationError('Employee %s is already assigned to position %s. You must'
                                      ' terminate the assingment by assingning a end date' % (previous_position.employee,
                                                                                              previous_position.position))
            except PositionAssignment.DoesNotExist:
                pass

        super(PositionAssignment, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                                                     update_fields=update_fields)


class CoachingSession(TimeStampedModel):
    employee = models.ForeignKey(Employee, related_name='coaching_sessions')
    coach = models.ForeignKey(Employee, related_name='coached_sessions')
    start_date_time = models.DateTimeField(default=timezone.now)
    end_date_time = models.DateTimeField(null=True, blank=True)
    comments = models.TextField()



    def time_spent(self):
        if self.end_date_time is None:
            return 0
        else:
            return self.end_date_time - self.start_date_time

    def get_absolute_url(self):
        return reverse('employee:coaching-detail', kwargs={'pk': self.pk})