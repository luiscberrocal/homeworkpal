from django.shortcuts import render

# Create your views here.
from django.views.generic import View, TemplateView
from employee.models import Employee


class MaximoView(TemplateView):

    template_name = 'maximo/show_sql.html'

    def get_context_data(self):
        base_where_clause = '((%s)) and ((startdate >= to_date (\'%s\' , \'YYYY-MM-DD\'))) and ((startdate <= to_date (\'%s\' , \'YYYY-MM-DD\'))) order by startdate desc'
        ctx = super(MaximoView, self).get_context_data()
        employees = Employee.objects.from_group('tino-ns')
        labor_code_condition = self._build_labor_condition(employees)
        start_date = '2015-10-01'
        end_date = '2015-10-30'
        ctx['sql'] = base_where_clause % (labor_code_condition, start_date, end_date)
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

