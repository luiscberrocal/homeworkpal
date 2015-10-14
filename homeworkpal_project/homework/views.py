from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Homework


class HomeworkListView(ListView):
    model = Homework

    def get_queryset(self):
        query_set = super(HomeworkListView, self).get_queryset()
        school_slug = self.kwargs['school_slug']
        level_slug = self.kwargs['school_level_slug']
        return query_set.filter(subject__school_level__school__slug__exact=school_slug,
                                subject__school_level__slug__exact=level_slug)
