from django.forms import ModelForm
from .models import CoachingSession

__author__ = 'LBerrocal'


class CoachingSessionForm(ModelForm):
    class Meta:
        model = CoachingSession
        fields = ['employee', 'start_date_time', 'end_date_time', 'comments']
