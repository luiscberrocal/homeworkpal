from braces.views import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from .serializers import EmployeeSerializer, UserSerializer, GroupSerializer, CompanyGroupSerializer
from .models import Employee, CompanyGroup


class EmployeeViewSet(viewsets.ModelViewSet):

    serializer_class = EmployeeSerializer

    def get_queryset(self):
        group_slug = self.request.query_params.get('group-slug', None)
        if group_slug:
            qs = Employee.objects.from_group(group_slug)
        else:
            qs = Employee.objects.all()

        return qs


class CompanyGroupViewSet(viewsets.ModelViewSet):
    queryset = CompanyGroup.objects.all()
    serializer_class = CompanyGroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee

    def get_queryset(self):
        qs = Employee.objects.from_group(self.kwargs['group_slug'])
        return qs


class EmployeeProjectsView(LoginRequiredMixin, DetailView):
    model = Employee
    context_object_name = 'employee'
    template_name = 'employee/employee_projects.html'


class EmployeeGoalsView(LoginRequiredMixin, DetailView):
    model = Employee
    context_object_name = 'employee'
    template_name = 'employee/employee_goals.html'