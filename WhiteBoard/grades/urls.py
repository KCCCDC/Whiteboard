from django.conf.urls import patterns, url

from WhiteBoard.grades import views

urlpatterns = patterns('',
	url(r'^assignments', views.assignments, name='assignments'),
	url(r'^create_assignment', views.CreateAssignmentView.as_view(), name='create_assignment'),
	url(r'^submit_assignment', views.submit_assignment, name='submit_assignment'),
	url(r'^edit_assignment', views.edit_assignment, name='edit_assignemtn'),
	url(r'^submissions', views.submissions, name='submissions'),
	url(r'^exams', views.exams, name='exams'),
	url(r'^create_exam', views.create_exam, name='create_exam'),
	url(r'^edit_exam', views.exams, name='edit_exam'),
	url(r'^add_question', views.edit_question, name='add_question'),
	url(r'^edit_question', views.edit_question, name='edit_question'),
	url(r'^take_exam', views.take_exam, name='take_exam'),
	url(r'^view_examsubmissions', views.view_examsubmissions, name='view_examsubmissions'),
	url(r'^grade_examsubmission', views.grade_examsubmissions, name='grade_examsubmissions'),
	url(r'^grades', views.grades, name='grades'),
)
