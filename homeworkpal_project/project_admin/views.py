from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
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