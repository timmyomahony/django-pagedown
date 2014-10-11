from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^upload/$', 'pagedown.views.upload_view', name='pagedown_upload'),
)
