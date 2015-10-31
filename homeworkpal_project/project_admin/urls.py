from django.conf.urls import patterns, url
from .views import ProjectListView, ProjectDetailView, ProjectUpdateView, ProjectCreateView, ProjectDeleteView

__author__ = 'LBerrocal'


urlpatterns = patterns('',
                       url(r'^$', ProjectListView.as_view(),kwargs= {'status': 'all'}, name='all_projects'),
                       url(r'^running/$', ProjectListView.as_view(), kwargs={'status': 'running'}, name='running_projects'),
                       url(r'^(?P<pk>[\d]*)/$', ProjectDetailView.as_view(), name='project_detail'),
                       url(r'^update/(?P<pk>[\d]*)/$', ProjectUpdateView.as_view(), name='project_update'),
                       url(r'^create/$', ProjectCreateView.as_view(), name='project_create'),
                        url(r'^delete/(?P<pk>[\d]*)/$', ProjectDeleteView.as_view(), name='project_delete'),
                       )