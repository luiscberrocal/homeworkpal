from braces.views import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from rest_framework import viewsets
from employee.forms import CoachingSessionForm
from .serializers import EmployeeSerializer, UserSerializer, GroupSerializer, CompanyGroupSerializer
from .models import Employee, CompanyGroup, CoachingSession


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

class CoachingSessionUpdateView(LoginRequiredMixin, UpdateView):
    model = CoachingSession
    context_object_name = 'coaching_session'
    form_class = CoachingSessionForm


class CoachingSessionCreateView(LoginRequiredMixin, CreateView):
    model = CoachingSession
    context_object_name = 'coaching_session'
    form_class = CoachingSessionForm

    def get_context_data(self, **kwargs):
        context = super(CoachingSessionCreateView, self).get_context_data(**kwargs)
        context['form'].fields['employee'].queryset = Employee.objects.from_group(self.kwargs['group_slug'])
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        employee = Employee.objects.get(user=self.request.user)
        obj.coach = employee
        obj.save()
        return super(CoachingSessionCreateView, self).form_valid(form)


class CoachingSessionDetailView(LoginRequiredMixin, DetailView):
    model = CoachingSession
    context_object_name = 'coaching_session'
