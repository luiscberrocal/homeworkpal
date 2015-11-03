from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.forms import inlineformset_factory
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from rest_framework import viewsets
from .models import Project, ProjectMember, Risk
from .forms import ProjectForm, RiskLineFormSet, ProjectMemberLineFormSet
from .mixins import AbstractProjectCreateUpdateMixin
from .serializers import ProjectMemberSerializer, ProjectSerializer


class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project

    def get_queryset(self):
        query_set = super(ProjectListView, self).get_queryset()
        if self.kwargs['status'] == 'running':
            query_set = query_set.filter(actual_start_date__isnull=False)
        return query_set
        #return query_set.filter(actual_start_date__isnull=False)

    def status(self):
        return self.kwargs['status']


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        ctx = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = self.get_object()
        ctx['members'] = ProjectMember.objects.assigned_to_project(project)
        return ctx


class ProjectUpdateView(LoginRequiredMixin, AbstractProjectCreateUpdateMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    formset_classes = (('line_formset',RiskLineFormSet),
                       ('members_formset', ProjectMemberLineFormSet),)


class ProjectCreateView(LoginRequiredMixin, AbstractProjectCreateUpdateMixin, CreateView):
    model = Project
    form_class = ProjectForm
    formset_classes = (('line_formset',RiskLineFormSet),
                       ('members_formset', ProjectMemberLineFormSet),)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('project:all_projects')



