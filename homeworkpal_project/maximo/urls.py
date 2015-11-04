from django.conf.urls import patterns, url
from maximo.views import MaximoView

__author__ = 'LBerrocal'
urlpatterns = patterns('',
                       url(r'^sql/$', MaximoView.as_view(), name='maximo-where'),
                       )