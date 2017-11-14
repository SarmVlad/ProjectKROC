from django.conf.urls import url

from MainApp import views

urlpatterns = [
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<city>.+)/(?P<method>[a-z]+$)',
    views.index),
url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<city>.+$)',
    views.index)
]