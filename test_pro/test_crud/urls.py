from django.conf.urls.defaults import *

urlpatterns = patterns('test_crud.views',
    (r'^dashboard/$', 'dashboard'),
    (r'^upload/(?P<fileType>.+)/$', 'upload'),
    (r'^update/(?P<fileType>.+)/$', 'update'),
    (r'^delete/(?P<fileType>.+)/$', 'delete'),
    (r'^search/$', 'search'),
)

