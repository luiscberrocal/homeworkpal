from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from employee.models import Employee
from project_admin.models import Project


class MaximoTicket(TimeStampedModel):
    MAXIMO_SR = 'SR'
    MAXIMO_WORKORDER = 'WO'
    MAXIMO_TICKET_TYPES = ((MAXIMO_SR, _('Service Request')),
                           (MAXIMO_WORKORDER, _('Work Order')))
    ticket_type = models.CharField(max_length=2, choices=MAXIMO_TICKET_TYPES, default=MAXIMO_SR)
    number = models.CharField(max_length=7, validators=[RegexValidator(regex=r'\d{6}')])
    name = models.CharField(max_length=120)
    is_open = models.BooleanField(default=True)
    project = models.ForeignKey(Project, related_name='maximo_tickets', null=True, blank=True)

    class Meta:
        ordering = ('number',)
        unique_together = ('ticket_type', 'number')

    def __str__(self):
        return '%s %s' % (self.ticket_type, self.number)


class MaximoTimeRegister(TimeStampedModel):
    employee = models.ForeignKey(Employee, related_name='maximo_time_registers')
    ticket = models.ForeignKey(MaximoTicket, related_name='time_registers')
    project = models.ForeignKey(Project, related_name='maximo_time_registers', null=True, blank=True)
    date = models.DateField()
    regular_hours = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(null=True, blank=True)
