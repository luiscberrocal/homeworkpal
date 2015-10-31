from django.core.urlresolvers import reverse_lazy
from django.forms import inlineformset_factory
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Project, ProjectMember, Risk
from .forms import RiskFormSet


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

    def get_context_data(self, **kwargs):
        ctx = super(ProjectUpdateView, self).get_context_data(**kwargs)
        ctx['risk_form'] = RiskFormSet()
        return ctx


class ProjectCreateView(CreateView):
    model = Project
    fields = ['short_name', 'description', 'planned_start_date',
              'planned_end_date', 'actual_start_date', 'actual_end_date',
              'planned_man_hours', 'type', 'group', 'priority']


    def get_context_data(self, **kwargs):
        ctx = super(ProjectCreateView, self).get_context_data(**kwargs)
        ctx['risk_form'] = RiskFormSet()
        return ctx

class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('project:all_projects')



