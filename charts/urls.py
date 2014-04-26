from django.conf.urls import patterns, url
from charts import views

urlpatterns = patterns('',
    url(r'^add/$', views.add_issue, name='add_issue'),
    url(r'^$', views.index, name='index'),
)
