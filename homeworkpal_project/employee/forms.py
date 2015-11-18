from datetimewidget.widgets import DateWidget, DateTimeWidget
from django.forms import ModelForm
from .models import CoachingSession

__author__ = 'LBerrocal'


class CoachingSessionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CoachingSessionForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['employee'].widget.attrs['readonly'] = True
            self.fields['employee'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = CoachingSession
        fields = ['employee', 'start_date_time', 'end_date_time', 'comments']
        date_time_options = {
            'todayBtn': 'true',
            'showMeridian': True,
        }
        widgets = {
            # Use localization and bootstrap 3
            'start_date_time': DateTimeWidget(options=date_time_options, attrs={'id': "start-date-time"}, usel10n=True, bootstrap_version=3),
            'end_date_time': DateTimeWidget(options=date_time_options, attrs={'id': "end-date-time"}, usel10n=True, bootstrap_version=3)
        }
