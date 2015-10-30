from datetimewidget.widgets import DateTimeWidget
from django.forms import forms
from .models import Project

__author__ = 'luiscberrocal'

class ProjectForm(forms.ModelForm):
    model = Project
    widgets = {
            #Use localization and bootstrap 3
            'datetime': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3)
        }

