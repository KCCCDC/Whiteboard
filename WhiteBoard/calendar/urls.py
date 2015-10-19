from django.conf.urls import patterns, url

from WhiteBoard.calendar import views

urlpatterns = patterns('',
    url(r'^calendar', views.calendar, name='calendar'),
    url(r'^create_event', views.edit_event, name='create_event'),
    url(r'^edit_event', views.edit_event, name='edit_event'),
)
