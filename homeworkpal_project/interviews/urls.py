from django.conf.urls import patterns, url
from interviews.views import ElegibilityCertificateDetailView

__author__ = 'LBerrocal'

urlpatterns = patterns('',
                       url(r'^certificate/(?P<pk>[\d]+)/$', ElegibilityCertificateDetailView.as_view(), name='certificate-goal'),
                       )