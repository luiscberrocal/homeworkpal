from datetimewidget.widgets import DateTimeWidget
from django.forms import forms, inlineformset_factory
from .models import Project, Risk

__author__ = 'luiscberrocal'

RiskFormSet = inlineformset_factory(Project, Risk,
                                    fields=['risk_type', 'priority', 'description'],
                                    extra=1)
