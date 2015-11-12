from django import forms
from django.utils.translation import ugettext_lazy as _
from maximo.excel import MaximoExcelData
from .models import DataDocument

__author__ = 'lberrocal'


class DataDocumentForm(forms.ModelForm):
    LOAD_CHOICES = ((MaximoExcelData.LOAD_ALL, _('Load All')),
                    (MaximoExcelData.LOAD_TICKETS, _('Load Tickets')),
                    (MaximoExcelData.LOAD_TIME, _('Load Time'))
                    )
    load_type = forms.ChoiceField(choices=LOAD_CHOICES, label=_('Load Type'))
    class Meta:
        model = DataDocument
        fields = ('docfile',)




