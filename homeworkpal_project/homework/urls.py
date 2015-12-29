from django.conf.urls import patterns, url
from .views import HomeworkListView

__author__ = 'LBerrocal'

urlpatterns = patterns('',
                       url(regex=r'^$',
                           view=HomeworkListView.as_view(),
                           name='list'),
                       url(regex=r'^(?P<school_slug>[\w\-]*)/(?P<school_level_slug>[\w\-]*)/$',
                           view=HomeworkListView.as_view(),
                           name='list'),
                       )