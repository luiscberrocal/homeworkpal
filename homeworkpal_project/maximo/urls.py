from django.conf.urls import patterns, url
from .views import MaximoView, DataDocumentCreateView, DataDocumentListView

__author__ = 'LBerrocal'
urlpatterns = patterns('',
                       url(r'^sql/$', MaximoView.as_view(), name='maximo-where'),
                       url(r'^upload/$', DataDocumentCreateView.as_view(), name='load-data'),
                       url(r'^upload/list/$', DataDocumentListView.as_view(), name='upload-list'),
                       )