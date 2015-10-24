from django.conf import settings
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


class PositionAssignment(models.Model):
    position = models.ForeignKey(Position)
    employee = models.ForeignKey(Employee)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
