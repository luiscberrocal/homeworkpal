from datetimewidget.widgets import DateTimeWidget
from django.forms import forms, inlineformset_factory, BaseFormSet, ModelForm, BaseInlineFormSet
from .models import Project, Risk, ProjectMember

__author__ = 'luiscberrocal'

class RequiredFirstInlineFormSet(BaseInlineFormSet):
    """
    Used to make empty formset forms required
    See http://stackoverflow.com/questions/2406537/django-formsets-\
        make-first-required/4951032#4951032
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.forms) > 0:
            first_form = self.forms[0]
            first_form.empty_permitted = False


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['short_name', 'description', 'planned_start_date',
                  'planned_end_date', 'actual_start_date', 'actual_end_date',
                  'planned_man_hours', 'type', 'group', 'priority']


class ProjectMemberLineForm(ModelForm):
    class Meta:
        model = ProjectMember
        fields = ['role', 'employee', 'start_date', 'end_date']


class RiskLineForm(ModelForm):
    class Meta:
        model = Risk
        fields = ['risk_type','priority','description']

RiskLineFormSet = inlineformset_factory(Project, Risk, form=RiskLineForm, formset=RequiredFirstInlineFormSet,
                                    extra=1)

ProjectMemberLineFormSet = inlineformset_factory(Project, ProjectMember,
                                                 form = ProjectMemberLineForm,
                                                 formset=RequiredFirstInlineFormSet, extra=1)