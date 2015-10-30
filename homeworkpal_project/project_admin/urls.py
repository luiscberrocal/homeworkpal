from django.conf.urls import patterns, url
from .views import ProjectListView, ProjectDetailView, ProjectUpdateView

__author__ = 'LBerrocal'


urlpatterns = patterns('',
                       url(r'^$', ProjectListView.as_view(), {'status': 'all'}),
                       url(r'^running/$', ProjectListView.as_view(), {'status': 'running'}),
                       url(r'^(?P<pk>[\d]*)/$', ProjectDetailView.as_view(), name='project_detail'),
                       url(r'^update/(?P<pk>[\d]*)/$', ProjectUpdateView.as_view(), name='project_update')
                       )