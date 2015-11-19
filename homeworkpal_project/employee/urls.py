from django.conf.urls import patterns, url
from .views import EmployeeListView, EmployeeProjectsView, EmployeeGoalsView, CoachingSessionCreateView, \
    CoachingSessionDetailView, CoachingSessionUpdateView, CoachingSessionListView

__author__ = 'LBerrocal'


urlpatterns = patterns('',
                       url(r'^goals/(?P<pk>[\d]+)/$', EmployeeGoalsView.as_view(), name='employee-goals'),
                       url(r'^coaching/(?P<group_slug>[a-z-]+)/create/$', CoachingSessionCreateView.as_view(), name='create-coaching'),
                       url(r'^coaching/(?P<pk>[\d]+)/$', CoachingSessionDetailView.as_view(), name='coaching-detail'),
                       url(r'^coaching/(?P<pk>[\d]+)/update$', CoachingSessionUpdateView.as_view(), name='coaching-update'),
                       url(r'^coaching/(?P<group_slug>[a-z-]+)/list.html$', CoachingSessionListView.as_view(), name='coaching-list'),
                       url(r'^list/(?P<group_slug>[a-z-]+)/$',EmployeeListView.as_view(), name='list-group-employees'),
                       url(r'^(?P<pk>[\d]+)/$', EmployeeProjectsView.as_view(), name='employee-projects'),
                       )