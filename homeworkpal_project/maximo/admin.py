from django.contrib import admin

# Register your models here.
from .models import DataDocument, MaximoTicket, MaximoTimeRegister


class MaximoTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_type', 'number', 'name', 'is_open', 'project', 'created']

class MaximoTimeRegisterAdmin(admin.ModelAdmin):
    list_display = ['employee', 'ticket', 'date', 'regular_hours', 'pay_rate', 'created']
    list_filter = (
        ('employee', admin.RelatedOnlyFieldListFilter),
    )

admin.site.register(DataDocument)
admin.site.register(MaximoTicket, MaximoTicketAdmin)
admin.site.register(MaximoTimeRegister, MaximoTimeRegisterAdmin)