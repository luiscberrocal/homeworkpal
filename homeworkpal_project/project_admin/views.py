from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, UpdateView
from .models import Project


class ProjectListView(ListView):
    model = Project

    def get_queryset(self):
        query_set = super(ProjectListView, self).get_queryset()
        if self.kwargs['status'] == 'running':
            query_set = query_set.filter(actual_start_date__isnull=False)
        return query_set
        #return query_set.filter(actual_start_date__isnull=False)


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'

class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['short_name', 'description', 'planned_start_date', 'planned_end_date', 'actual_start_date']

    # actual_end_date = models.DateField(null=True, blank=True)
    # slug = AutoSlugField(populate_from='short_name', max_length=60, unique=True)
    # planned_man_hours = models.DecimalField(max_digits=7, decimal_places=2)
    # type = models.CharField(max_length=8, choices=PROJECT_TYPES, default=MAIN_PROJECT)
    # group = models.ForeignKey(CompanyGroup, null=True)
    # priority = models.IntegerField(default=10, help_text='The lower the number the higher the priority')
