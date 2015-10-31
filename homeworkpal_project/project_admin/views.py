from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Project, ProjectMember


class ProjectListView(ListView):
    model = Project

    def get_queryset(self):
        query_set = super(ProjectListView, self).get_queryset()
        if self.kwargs['status'] == 'running':
            query_set = query_set.filter(actual_start_date__isnull=False)
        return query_set
        #return query_set.filter(actual_start_date__isnull=False)

    def status(self):
        return self.kwargs['status']


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        ctx = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = self.get_object()
        ctx['members'] = ProjectMember.objects.assigned_to_project(project)
        return ctx


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['short_name', 'description', 'planned_start_date',
              'planned_end_date', 'actual_start_date', 'actual_end_date',
              'planned_man_hours', 'type', 'group', 'priority']


class ProjectCreateView(CreateView):
    model = Project
    fields = ['short_name', 'description', 'planned_start_date',
              'planned_end_date', 'actual_start_date', 'actual_end_date',
              'planned_man_hours', 'type', 'group', 'priority']

class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('project:all_projects')
