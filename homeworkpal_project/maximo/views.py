import datetime
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.generic import View, TemplateView, CreateView, ListView, DetailView
from employee.models import Employee, CompanyGroup
from maximo.excel import MaximoExcelData
from maximo.forms import DataDocumentForm
from maximo.models import DataDocument
from maximo.tasks import ProcessExcelTask


class MaximoView(TemplateView):

    template_name = 'maximo/show_sql.html'

    def get_context_data(self):
        #base_where_clause = '((%s)) and ((startdate >= to_date (\'%s\' , \'YYYY-MM-DD\'))) and ((startdate <= to_date (\'%s\' , \'YYYY-MM-DD\'))) order by startdate desc'

        where_parts = list()
        where_parts.append('((')
        where_parts.append('')
        where_parts.append(mark_safe(')) and ((startdate >= TO_DATE (\''))
        where_parts.append('')
        where_parts.append(mark_safe('\' , \'YYYY-MM-DD\'))) and ((startdate <= TO_DATE (\''))
        where_parts.append('')
        where_parts.append(mark_safe('\' , \'YYYY-MM-DD\'))) order by startdate desc'))

        ctx = super(MaximoView, self).get_context_data()
        employees = Employee.objects.from_group('tino-ns')

        labor_code_condition = self._build_labor_condition(employees)
        where_parts[1] = mark_safe(labor_code_condition)
        where_parts[3] = '2015-10-01'
        where_parts[5] = datetime.date.today().strftime('%Y-%m-%d')

        ctx['employees'] = employees
        ctx['where_parts'] = where_parts
        ctx['start_date'] = where_parts[3]
        ctx['end_date'] = where_parts[5]
        ctx['sql'] = ''.join(where_parts)  #base_where_clause % (labor_code_condition, ctx['start_date'], ctx['end_date'])
        return ctx

    def _build_labor_condition(self, employees):
        labor_code_condition = ''
        count = 1
        for employee in employees:
            labor_code_condition += 'laborcode=\'%s\'' % employee.user.username.upper()
            if len(employees) > 1:
                if count != len(employees):
                    labor_code_condition += ' or '
            count += 1
        return labor_code_condition


class DataDocumentDetailView(LoginRequiredMixin, DetailView):
    model = DataDocument
    context_object_name = 'datadocument'


class DataDocumentListView(LoginRequiredMixin, ListView):
    model = DataDocument


class DataDocumentCreateView(LoginRequiredMixin, CreateView):
    model = DataDocument
    form_class = DataDocumentForm
    success_url = reverse_lazy('maximo:upload-list')

    def form_valid(self, form):
        ext = form.instance.docfile.name.split('.')[1]
        form.instance.extension = ext
        form.save()
        ProcessExcelTask.delay(form.instance.pk, form.cleaned_data['load_type'])
        # form.instance.date_start_processing = timezone.now()
        # data_loader = MaximoExcelData()
        # results = data_loader.load(form.instance.docfile.file)
        # form.instance.results = results
        return super(DataDocumentCreateView, self).form_valid(form)
