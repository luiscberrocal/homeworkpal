from django.conf.urls import patterns, url
from .views import EmployeeListView

__author__ = 'LBerrocal'

urlpatterns = patterns('',
                       url(r'^(?P<group_slug>[a-z-]*)/list/$',EmployeeListView.as_view(), name='list-group-employees'),
                       )