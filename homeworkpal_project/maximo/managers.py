from django.db import models
from django.db.models import Sum, Count

__author__ = 'lberrocal'

class MaximoTimeRegisterManager(models.Manager):

    def get_emloyee_total_regular_hours(self, employee, work_date):
        qs = self.get_queryset()
        return qs.filter(employee=employee,date=work_date).aggregate(total_regular_hours=Sum('regular_hours'),
                                                                     register_count=Count('regular_hours'))
