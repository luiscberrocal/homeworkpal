from django import forms
from .models import CoachingSession

__author__ = 'LBerrocal'


class CoachingSessionForm(forms.Form):
    class Meta:
        model = CoachingSession
        fields = ['employee','start_date_time', 'end_date_time', 'comments']
