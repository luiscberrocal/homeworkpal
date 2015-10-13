from django.conf.urls import patterns, url
from .views import HomeworkListView

__author__ = 'LBerrocal'

urlpatterns = patterns('',
                       url(regex=r'^$',
                           view=HomeworkListView.as_view(),
                           name='list'),
                       )