from datetime import date
from django.contrib import admin

# Register your models here.
from django.contrib.admin import SimpleListFilter

from .models import DataDocument, MaximoTicket, MaximoTimeRegister

class FiscalYearFilter(SimpleListFilter):

    title = 'fiscal year'

    parameter_name = 'fiscal_year'

    def lookups(self, request, model_admin):
        return (('FY15', 'FY ma2015'), ('FY16', 'FY 2016'))

    def queryset(self, request, queryset):
        if self.value() == 'FY15':
            return queryset.filter(date__gte=date(2014,10,1), date__lte=date(2015, 9,30))
        if self.value() == 'FY16':
            return queryset.filter(date__gte=date(2015, 10, 1), date__lte=date(2016, 9, 30))


class MaximoTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_type', 'number', 'name', 'is_open', 'project', 'created']

class MaximoTimeRegisterAdmin(admin.ModelAdmin):
    list_display = ['employee', 'ticket', 'date', 'regular_hours', 'pay_rate', 'created']
    list_filter = (
        ('employee', admin.RelatedOnlyFieldListFilter), FiscalYearFilter
    )

admin.site.register(DataDocument)
admin.site.register(MaximoTicket, MaximoTicketAdmin)
admin.site.register(MaximoTimeRegister, MaximoTimeRegisterAdmin)