from django.conf.urls import patterns, url
from charts import views

urlpatterns = patterns('',
    url(r'^issues/$', views.issue_index, name='issue_index'),
    url(r'^issues/add/$', views.add_issue, name='add_issue'),
    url(r'^issues/(?P<issue_id>\d+)/$', views.issue_detail, name='issue_detail'),
    url(r'^issues/(?P<issue_id>\d+)/edit/$', views.edit_issue, name='edit_issue'),
    url(r'^account/login/$', views.login_view, name='login_view'),
    url(r'^account/logout/$', views.logout_view, name='logout_view'),
    url(r'^account/register/$', views.register_view, name='register_view'),
    url(r'^people/$', views.people_index, name='people_index'),
    url(r'^people/(?P<person_id>\w+)/$', views.person_detail, name='person_detail'),
    url(r'^commits/$', views.commits_index, name='commits_index'),
    url(r'^$', views.index, name='index'),
)
