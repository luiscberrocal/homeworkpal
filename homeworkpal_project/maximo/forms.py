from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import DataDocument

__author__ = 'lberrocal'

class DataDocumentForm(forms.ModelForm):
    class Meta:
        model = DataDocument
        fields = ('docfile',)




