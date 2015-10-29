from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Project


class ProjectListView(ListView):
    model = Project