from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
PERMANENT_TYPE = 'PERM'
TEMPORARY_TYPE = 'TEMP'
TENURE_TYPES = (
    (PERMANENT_TYPE, 'Permanent'),
    (TEMPORARY_TYPE, 'Temporary')
    )


class Position(models.Model):
    number = models.CharField(max_length=6, unique=True)
    grade = models.CharField(max_length=5)
    type = models.CharField(max_length=4, choices=TENURE_TYPES)

    def __str__(self):
        return '%s %s' % (self.number, self.grade)


class Employee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    company_id = models.CharField(max_length=7)
    tenure = models.CharField(max_length=4, choices=TENURE_TYPES)

    def _group(self):
        try:
            group_assignment = CompanyGroupEmployeeAssignment.objects.get(employee=self, end_date=None)
            group = group_assignment.group
        except CompanyGroupEmployeeAssignment.DoesNotExist:
            group = None
        return group
    group = property(_group)

    def __str__(self):
        if self.user.last_name and self.user.first_name:
            return '%s, %s' % (self.user.last_name, self.user.first_name)
        else:
            return self.user.username


class CompanyGroup(models.Model):
    name = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=120, null=True, blank=True)
    parent_group = models.ForeignKey('self', null=True, blank=True )

    def __str__(self):
        return self.name


class CompanyGroupEmployeeAssignment(models.Model):
    group = models.ForeignKey(CompanyGroup)
    employee = models.ForeignKey(Employee)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            previous_group = CompanyGroupEmployeeAssignment.objects.get(employee=self.employee,
                                                                        end_date=None)
            raise ValidationError('Employee %s is already assigned to group %s. You must'
                                   ' terminate the assingment by assingning a end date' % (previous_group.employee, previous_group.group))
        except CompanyGroupEmployeeAssignment.DoesNotExist:
            super(CompanyGroupEmployeeAssignment, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                                                 update_fields=update_fields)




class PositionAssignment(models.Model):
    position = models.ForeignKey(Position)
    employee = models.ForeignKey(Employee)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
