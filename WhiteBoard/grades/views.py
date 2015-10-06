from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.templatetags.static import static
from django.contrib.auth import authenticate, login as authLogin, logout as authLogout, update_session_auth_hash
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password, is_password_usable
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from WhiteBoard.base.models import Person
from .models import GradableItem, Submission, ExamQuestion
from .forms import AssignmentForm, SubmissionForm, GradeAssignmentForm, ExamForm, ExamQuestionForm
from WhiteBoard.base.helpers import getRole

from os import listdir
from os.path import isfile, join

def assignments(request):
	assignments = GradableItem.objects.filter(type='HMWK')
	for assignment in assignments:
		submission = Submission.objects.filter(submitter_id = request.user.id,
				gradableItem_id = assignment.id)
		if submission.count() != 0:
			assignment.submission = submission[0]
		else:
			assignment.submission = ''
	return render(request, 'grades/assignments.html', {'assignments' : assignments, 'role' : getRole(request)})

def submit_assignment(request):
	id = request.GET['id']
	instance = Submission.objects.filter(gradableItem_id=id, submitter_id=request.user.id)
	if request.method == 'GET':
		if instance.count() == 0:
			form = SubmissionForm()
		else:
			form = SubmissionForm(instance=instance[0])
		return render(request, "file_upload_form.html", {'form' : form})
	elif request.method == 'POST':
		if instance.count() == 0:
			form = SubmissionForm(request.POST, request.FILES)
		else:
			form = SubmissionForm(request.POST, request.FILES, instance=instance[0])
		form.instance.gradableItem_id = id
		form.instance.submitter_id = request.user.id
		form.save()
		return HttpResponseRedirect(reverse('grades:assignments'))

def edit_assignment(request):
	id = request.GET['id']
	instance = GradableItem.objects.get(id=id);
	if request.method == 'GET':
		form = AssignmentForm(instance=instance)
		return render(request, "file_upload_form.html", {'form' : form})
	elif request.method == 'POST':
		form = AssignmentForm(request.POST, request.FILES, instance = instance)
		form.save()
		return HttpResponseRedirect(reverse('grades:assignments'))

class CreateAssignmentView(CreateView):
	template_name='file_upload_form.html'
	model = GradableItem 
	fields = ['max_score', 'title', 'description', 'due_date', 'file']
	success_url = '/assignments'

	def form_valid(self, form):
		form.instance.type = "HMWK"
		return super(CreateAssignmentView, self).form_valid(form)

def submissions(request):
	if 'submission' in request.GET and request.method == "GET":
		submission = request.GET['submission']
		instance = Submission.objects.get(id=submission)
		form = GradeAssignmentForm(instance=instance)
		return render(request, "grades/grade_assignment.html", {'form' : form, 'submission' : instance})
	elif 'submission' in request.GET and request.method == "POST":
		instance = Submission.objects.get(id=request.GET['submission'])
		form = GradeAssignmentForm(request.POST, instance=instance)
		form.instance.grader = Person.objects.get(user_id = request.user.id)
		form.save()
		assignment = Submission.objects.get(id=request.GET['submission']).gradableItem.id
		submissions = Submission.objects.filter(gradableItem_id = assignment)
	elif 'assignment' not in request.GET:
		assignment = ""
		submissions = ""
	else:
		assignment = GradableItem.objects.get(id = request.GET['assignment'])
		submissions = Submission.objects.filter(gradableItem_id = assignment)
	assignments = GradableItem.objects.filter(type="HMWK")
	return render(request, 'grades/submissions.html', {'assignment' : assignment, 'submissions' : submissions, \
		'assignments' : assignments})

def exams(request):
	if request.method == "GET":
		if 'exam' in request.GET:
			instance = GradableItem.objects.get(id=request.GET['exam'])
			form = ExamForm(instance=instance)
			questions = ExamQuestion.objects.filter(gradableItem=instance)
			return render(request, 'grades/exam_form.html', {'form' : form, 'exam' : instance, \
					'questions' : questions})
		else:
			exams = GradableItem.objects.filter(type="EXAM")
			return render(request, 'grades/exams.html', {'exams' : exams})
	elif request.method == "POST":
		if 'exam' in request.GET:
			print "HI"
			instance = GradableItem.objects.get(id=request.GET['exam'])
			form = ExamForm(request.POST, instance=instance)
			form.save()
			questions = ExamQuestion.objects.filter(gradableItem = instance)
			return render(request, 'grades/exam_form.html', {'form' : form, 'exam' : form.instance, \
					'questions' : questions})
		else:
			exams = GradableItem.objects.filter(type="EXAM")
			return render(request, 'grades/exams.html', {'exams' : exams})

def create_exam(request):
	if request.method == "GET":
		form = ExamForm()
		return render(request, 'base_form.html', {'form' : form})
	elif request.method == "POST":
		form = ExamForm(request.POST)
		form.instance.type = "EXAM"
		form.save()
		url = reverse('grades:exams')
		return HttpResponseRedirect(url + "?exam=" + str(form.instance.id))

def edit_question(request):
	if request.method == "GET":
		if 'question' in request.GET:
			instance = ExamQuestion.objects.get(id = request.GET['question'])
			form = ExamQuestionForm(instance=instance)
			return render(request, 'base_form.html', {'form' : form})
		elif 'exam' in request.GET:
			form = ExamQuestionForm()
			return render(request, 'base_form.html', {'form' : form})
	if request.method == "POST":
		if 'question' in request.GET:
			instance = ExamQuestion.objects.get(id = request.GET['question'])
			form = ExamQuestionForm(request.POST, instance=instance)
			form.save()
			url = reverse('grades:edit_exam')
			return HttpResponseRedirect(url + "?exam=" + str(instance.gradableItem_id))
		elif 'exam' in request.GET:
			form = ExamQuestionForm(request.POST)
			form.instance.gradableItem_id = request.GET['exam']
			form.instance.type = "TEXT" # TODO - add support for Multiple Choice
			form.save()
			url = reverse('grades:edit_exam')
			return HttpResponseRedirect(url + "?exam=" + str(form.instance.gradableItem_id))