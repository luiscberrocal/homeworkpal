from braces.views import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from interviews.models import ElegibilityCertificate


class ElegibilityCertificateDetailView(ElegibilityCertificate, DetailView):
    model = ElegibilityCertificate
    context_object_name = 'certificate'