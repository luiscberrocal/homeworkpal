from braces.views import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Employee


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee

    def get_queryset(self):
        qs = Employee.objects.from_group(self.kwargs['group_slug'])
        return qs
