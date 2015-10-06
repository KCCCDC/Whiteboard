from django.conf.urls import patterns, url

from WhiteBoard.grades import views

urlpatterns = patterns('',
	url(r'^assignments', views.assignments, name='assignments'),
	url(r'^create_assignment', views.CreateAssignmentView.as_view(), name='create_assignment'),
)
