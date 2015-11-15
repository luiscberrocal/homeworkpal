from django.db import models
from django.db.models import Sum, Count

__author__ = 'lberrocal'

# class MaximoTimeRegisterMixin(object):
#     def by_author(self, user):
#         return self.filter(user=user)
#
#     def published(self):
#         return self.filter(published__lte=datetime.now())
#
# class PostQuerySet(QuerySet, PostMixin):
#     pass

class MaximoTimeRegisterManager(models.Manager):
    def get_employee_total_regular_hours(self, employee, date):
        qs = self.get_queryset()
        return qs.filter(employee=employee, date=date).aggregate(total_regular_hours=Sum('regular_hours'),
                                                                 register_count=Count('regular_hours'))

    def assign_projects_from_ticket(self):
        qs = self.get_queryset()
        updated_count = 0
        for time_register in qs:
            if time_register.project is None:
                time_register.project = time_register.ticket.project
                time_register.save()
                updated_count += 1
        return updated_count

