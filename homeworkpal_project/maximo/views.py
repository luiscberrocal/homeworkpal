from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render

# Create your views here.
from django.utils.safestring import mark_safe
from django.views.generic import View, TemplateView, CreateView, ListView
from employee.models import Employee
from maximo.forms import DataDocumentForm
from maximo.models import DataDocument


class MaximoView(TemplateView):

    template_name = 'maximo/show_sql.html'

    def get_context_data(self):
        base_where_clause = '((%s)) and ((startdate >= to_date (\'%s\' , \'YYYY-MM-DD\'))) and ((startdate <= to_date (\'%s\' , \'YYYY-MM-DD\'))) order by startdate desc'

        where_parts = list()
        where_parts.append('((')
        where_parts.append('')
        where_parts.append(mark_safe(')) and ((startdate >= to_date (\''))
        where_parts.append('')
        where_parts.append(mark_safe('\' , \'YYYY-MM-DD\'))) and ((startdate <= to_date (\''))
        where_parts.append('')
        where_parts.append(mark_safe('\' , \'YYYY-MM-DD\'))) order by startdate desc'))

        ctx = super(MaximoView, self).get_context_data()
        employees = Employee.objects.from_group('tino-ns')
        labor_code_condition = self._build_labor_condition(employees)
        where_parts[1] = mark_safe(labor_code_condition)
        where_parts[3] = '2015-10-01'
        where_parts[5] = '2015-10-30'
        ctx['where_parts'] = where_parts
        ctx['start_date'] = where_parts[3]
        ctx['end_date'] = where_parts[5]
        ctx['sql'] = base_where_clause % (labor_code_condition, ctx['start_date'], ctx['end_date'])
        return ctx


    def _build_labor_condition(self, employees):
        labor_code_condition = ''
        count = 1
        for employee in employees:
            labor_code_condition += 'laborcode=\'%s\'' % employee.user.username.upper()
            if len(employees) > 1 and count != len(employees):
                labor_code_condition += ' or '
            count += 1
        return labor_code_condition


class DataDocumentListView(LoginRequiredMixin, ListView):
    model = DataDocument


class DataDocumentCreateView(LoginRequiredMixin, CreateView):
    model = DataDocument
    form_class = DataDocumentForm
    success_url = reverse_lazy('maximo:upload-list')

    def form_valid(self, form):
        ext = form.instance.docfile.name.split('.')[1]
        form.instance.extension = ext
        return super(DataDocumentCreateView, self).form_valid(form)