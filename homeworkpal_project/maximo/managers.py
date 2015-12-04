from django.db import models
from django.db.models import Sum, Count, QuerySet

__author__ = 'lberrocal'

class MaximoTimeRegisterMixin(object):

    def get_employee_total_regular_hours(self, employee, date):
        #qs = self.get_queryset()
        return self.filter(employee=employee, date=date).aggregate(total_regular_hours=Sum('regular_hours'),
                                                                 register_count=Count('regular_hours'))

    def assign_projects_from_ticket(self):
        #qs = self.get_queryset()
        updated_count = 0
        for time_register in self.filter():
            if time_register.project is None:
                time_register.project = time_register.ticket.project
                time_register.save()
                updated_count += 1
        return updated_count

    def sum_regular_hours(self):
        return self.filter().annotate(total_regular_hours=Sum('regular_hours'))


class MaximoTimeRegisterQuerySet(QuerySet, MaximoTimeRegisterMixin):
    pass

class MaximoTimeRegisterManager(models.Manager):

    def get_queryset(self):
        return MaximoTimeRegisterQuerySet(self.model, using=self._db)

    def assign_projects_from_ticket(self):
        return self.get_queryset().assign_projects_from_ticket()

    def get_employee_total_regular_hours(self, employee, date):
        return self.get_queryset().get_employee_total_regular_hours(employee, date)

    def sum_regular_hours(self, project):
        self.get_queryset().filter(project=project).sum_regular_hours()

