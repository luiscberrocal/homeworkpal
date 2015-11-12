from django.conf.urls import patterns, url
from .views import MaximoView, DataDocumentCreateView, DataDocumentListView, DataDocumentDetailView

__author__ = 'LBerrocal'
urlpatterns = patterns('',
                       url(r'^(?P<pk>[\d]*)/$', DataDocumentDetailView.as_view(), name='document-detail'),
                       url(r'^sql/$', MaximoView.as_view(), name='where-clause'),
                       url(r'^upload/$', DataDocumentCreateView.as_view(), name='load-data'),
                       url(r'^upload/list/$', DataDocumentListView.as_view(), name='upload-list'),
                       )