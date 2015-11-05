from django.conf.urls import patterns, url
from .views import MaximoView, DataDocumentCreateView

__author__ = 'LBerrocal'
urlpatterns = patterns('',
                       url(r'^sql/$', MaximoView.as_view(), name='maximo-where'),
                       url(r'^load/$', DataDocumentCreateView.as_view(), name='load-data'),
                       )