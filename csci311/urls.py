from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect
from django.contrib import admin
from charts.views import index_redirect
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index_redirect),
    url(r'^charts/', include('charts.urls')),
)