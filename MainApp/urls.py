from django.conf.urls import url

from MainApp import views

urlpatterns = [
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<lat>.+)/(?P<lon>.+)/(?P<method>[a-z]+$)',
    views.index),
url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<lat>.+)/(?P<lon>.+$)',
    views.index)
]