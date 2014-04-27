from django.conf.urls import patterns, url
from charts import views

urlpatterns = patterns('',
    url(r'^issues/$', views.issue_index, name='issue_index'),
    url(r'^issues/add/$', views.add_issue, name='add_issue'),
    url(r'^issues/(?P<issue_id>\d+)/$', views.issue_detail, name='issue_detail'),
    url(r'^issues/(?P<issue_id>\d+)/edit/$', views.edit_issue, name='edit_issue'),
    url(r'^$', views.index, name='index'),
)
