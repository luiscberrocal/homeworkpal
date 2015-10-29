from django.conf.urls import patterns, url
from .views import ProjectListView

__author__ = 'LBerrocal'


urlpatterns = patterns('',
                       url(r'^$', ProjectListView.as_view(), {'status': 'all'}),
                       url(r'^running/$', ProjectListView.as_view(), {'status': 'running'})
                       )