from os import listdir
from os.path import isfile, join

from django.core.urlresolvers import reverse
from django.contrib.auth import (authenticate, login as authLogin, logout
                                 as authLogout, update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import (check_password, make_password,
                                         is_password_usable)
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.templatetags.static import static
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView, CreateView

from .models import (GradableItem, Submission, ExamQuestion, ExamSubmission,
                     ExamAnswer)
from .forms import (AssignmentForm, SubmissionForm, GradeAssignmentForm,
                    ExamForm, ExamQuestionForm)
from WhiteBoard.base.helpers import getRole
from WhiteBoard.base.models import Person


@login_required(login_url='/loginRequired')
def assignments(request):
    assignments = GradableItem.objects.filter(type='HMWK')
    for assignment in assignments:
        submission = (Submission.objects.filter(submitter_id=request.user.id,
                      gradableItem_id=assignment.id))
        if submission.count() != 0:
            assignment.submission = submission[0]
        else:
            assignment.submission = ''
    return render(request, 'grades/assignments.html', {
        'assignments': assignments,
        'role': getRole(request),
        'isRedirect': False
    })


@login_required(login_url='/loginRequired')
def submit_assignment(request):
    id = request.GET['id']
    instance = (Submission.objects.filter(gradableItem_id=id,
                submitter_id=request.user.id))
    if request.method == 'GET':
        if instance.count() == 0:
            form = SubmissionForm()
            return render(request, "file_upload_form.html", {
                'form': form,
                'role': getRole(request)
            })
        else:
            form = SubmissionForm(instance=instance[0])
            assignments = GradableItem.objects.filter(type='HMWK')
            return render(request, 'grades/assignments.html', {
                'assignments': assignments,
                'role': getRole(request),
                'isRedirect': True
            })
    elif request.method == 'POST':
        if instance.count() == 0:
            form = SubmissionForm(request.POST, request.FILES)
        else:
            form = (SubmissionForm(request.POST, request.FILES,
                    instance=instance[0]))
        form.instance.gradableItem_id = id
        form.instance.submitter_id = request.user.id
        form.save()
        return HttpResponseRedirect(reverse('grades:assignments'))


@login_required(login_url='/loginRequired')
def edit_assignment(request):
    id = request.GET['id']
    instance = GradableItem.objects.get(id=id)
    if request.method == 'GET':
        form = AssignmentForm(instance=instance)
        return (render(request, "file_upload_form.html", {
            'form': form,
            'role': getRole(request)
        }))
    elif request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=instance)
        form.save()
        return HttpResponseRedirect(reverse('grades:assignments'))


class CreateAssignmentView(CreateView):
    template_name = 'file_upload_form.html'
    model = GradableItem
    fields = ['max_score', 'title', 'description', 'due_date', 'file']
    success_url = '/assignments'

    def dispatch(self, *args, **kwargs):
        return super(CreateAssignmentView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.type = "HMWK"
        return super(CreateAssignmentView, self).form_valid(form)


@login_required(login_url='/loginRequired')
def submissions(request):
    if 'submission' in request.GET and request.method == "GET":
        submission = request.GET['submission']
        instance = Submission.objects.get(id=submission)
        form = GradeAssignmentForm(instance=instance)
        return (render(request, "grades/grade_assignment.html", {
            'form': form,
            'submission': instance,
            'role': getRole(request)
        }))
    elif 'submission' in request.GET and request.method == "POST":
        instance = Submission.objects.get(id=request.GET['submission'])
        form = GradeAssignmentForm(request.POST, instance=instance)
        form.instance.grader = Person.objects.get(user_id=request.user.id)
        form.save()
        assignment = (Submission.objects.get(id=request.GET['submission'])
                      .gradableItem.id)
        submissions = Submission.objects.filter(gradableItem_id=assignment)
    elif 'assignment' not in request.GET:
        assignment = ""
        submissions = ""
    else:
        assignment = GradableItem.objects.get(id=request.GET['assignment'])
        submissions = Submission.objects.filter(gradableItem_id=assignment)
    assignments = GradableItem.objects.filter(type="HMWK")
    return (render(request, 'grades/submissions.html', {
        'assignment': assignment,
        'submissions': submissions,
        'assignments': assignments,
        'role': getRole(request)
    }))


@login_required(login_url='/loginRequired')
def exams(request):
    if request.method == "GET":
        if 'exam' in request.GET:
            instance = GradableItem.objects.get(id=request.GET['exam'])
            form = ExamForm(instance=instance)
            questions = ExamQuestion.objects.filter(gradableItem=instance)
            return (render(request, 'grades/exam_form.html', {
                'form': form,
                'exam': instance,
                'questions': questions,
                'role': getRole(request)
            }))
        else:
            exams = GradableItem.objects.filter(type="EXAM")
            person = Person.objects.get(user=request.user)
            for exam in exams:
                if person.type == "STUD":
                    submission = (ExamSubmission.objects.filter(
                                  gradableItem=exam, submitter=person)
                                  .order_by('date_submitted'))
                    if submission.count() > 0:
                        exam.submission = submission[0]
                    else:
                        exam.submission = ''
                else:
                    exam.submission = ''
            return (render(request, 'grades/exams.html', {
                'exams': exams,
                'role': getRole(request)
            }))
    elif request.method == "POST":
        if 'exam' in request.GET:
            print "HI"
            instance = GradableItem.objects.get(id=request.GET['exam'])
            form = ExamForm(request.POST, instance=instance)
            form.save()
            questions = ExamQuestion.objects.filter(gradableItem=instance)
            return (render(request, 'grades/exam_form.html', {
                'form': form,
                'exam': form.instance,
                'questions': questions,
                'role': getRole(request)
            }))
        else:
            exams = GradableItem.objects.filter(type="EXAM")
            return (render(request, 'grades/exams.html', {
                'exams': exams,
                'role': getRole(request)
            }))


@login_required(login_url='/loginRequired')
def create_exam(request):
    if request.method == "GET":
        form = ExamForm()
        return (render(request, 'base_form.html', {
            'form': form,
            'role': getRole(request)
        }))
    elif request.method == "POST":
        form = ExamForm(request.POST)
        form.instance.type = "EXAM"
        form.save()
        url = reverse('grades:exams')
        return HttpResponseRedirect(url + "?exam=" + str(form.instance.id))


@login_required(login_url='/loginRequired')
def edit_question(request):
    if request.method == "GET":
        if 'question' in request.GET:
            instance = ExamQuestion.objects.get(id=request.GET['question'])
            form = ExamQuestionForm(instance=instance)
            return (render(request, 'base_form.html', {
                'form': form,
                'role': getRole(request)
            }))
        elif 'exam' in request.GET:
            form = ExamQuestionForm()
            return render(request, 'base_form.html', {
                'form': form,
                'role': getRole(request)
            })
    if request.method == "POST":
        if 'question' in request.GET:
            instance = ExamQuestion.objects.get(id=request.GET['question'])
            form = ExamQuestionForm(request.POST, instance=instance)
            form.save()
            url = reverse('grades:edit_exam')
            return (HttpResponseRedirect(
                    url + "?exam=" + str(instance.gradableItem_id)))
        elif 'exam' in request.GET:
            form = ExamQuestionForm(request.POST)
            form.instance.gradableItem_id = request.GET['exam']
            form.instance.type = "TEXT"  # TODO add support for Multiple Choice
            form.save()
            url = reverse('grades:edit_exam')
            return (HttpResponseRedirect(
                    url + "?exam=" + str(form.instance.gradableItem_id)))


@login_required(login_url='/loginRequired')
def take_exam(request):
    if 'exam' not in request.GET:
        return HttpResponseRedirect(reverse('grades:exams'))
    if request.method == "GET":
        questions = (ExamQuestion.objects.filter(
                        gradableItem_id=request.GET['exam']))
        person = Person.objects.get(user=request.user)
        submission = (ExamSubmission.objects.filter(
                        gradableItem=request.GET['exam'], submitter=person))
        if submission.count() > 0:
            taken = 1
        else:
            taken = 0
        return (render(request, 'grades/take_exam.html', {
                                'questions': questions,
                                'taken': taken,
                                'role': getRole(request)
        }))
    elif request.method == "POST":
        submitter = Person.objects.get(user=request.user)
        examSubmission = ExamSubmission(
                                submitter=submitter,
                                gradableItem_id=request.GET['exam']
                            )
        examSubmission.save()
        questions = (ExamQuestion.objects.filter(
                    gradableItem_id=request.GET['exam']))
        for question in questions:
            answer = request.POST[str(question.id)]
            examAnswer = ExamAnswer(
                                examSubmission=examSubmission,
                                answer=answer,
                                examQuestion=question
                            )
            examAnswer.save()
        return HttpResponseRedirect(reverse('grades:exams'))


@login_required(login_url='/loginRequired')
def view_examsubmissions(request):
    if 'exam' not in request.GET:
        return HttpResponseRedirect(reverse('grades:exams'))
    if request.method == "GET":
        submissions = (ExamSubmission.objects.filter(
                      gradableItem_id=request.GET['exam']))

        for submission in submissions:
            questions = ExamAnswer.objects.filter(examSubmission=submission)
            submission.score = 0
            for question in questions:
                if question.points is not None:
                    submission.score += int(question.points)
                else:
                    score = ''
                    break
        return (render(request, 'grades/view_examsubmissions.html', {
            'submissions': submissions,
            'role': getRole(request)
        }))


@login_required(login_url='/loginRequired')
def grade_examsubmissions(request):
    submission = ExamSubmission.objects.get(id=request.GET['submission'])
    answers = ExamAnswer.objects.filter(examSubmission=submission)
    if request.method == "GET":
        return (render(request, "grades/grade_examsubmission.html", {
            'submission': submission,
            'answers': answers,
            'role': getRole(request)
        }))
    elif request.method == "POST":
        grader = Person.objects.get(user=request.user)
        for answer in answers:
            answer.points = (request.POST[str(answer.examQuestion.id) +
                             "_score"])
            answer.comment = (request.POST[str(answer.examQuestion.id) +
                              "_comment"])
            answer.grader = grader
            answer.save()
        return (HttpResponseRedirect(reverse(
                    "grades:view_examsubmissions") +
                    "?exam=" +
                    str(submission.gradableItem_id)
                ))


@login_required(login_url='/loginRequired')
def grades(request):
    person = Person.objects.get(user=request.user)
    exam_grades = ExamSubmission.objects.filter(submitter=person)
    for exam in exam_grades:
        answers = ExamAnswer.objects.filter(examSubmission=exam)
        exam.score = 0
        for answer in answers:
            if answer.points is not None:
                exam.score += int(answer.points)
            else:
                exam.score = None
                break
    assignment_grades = Submission.objects.filter(submitter=person)
    return (render(request, "grades/grades.html", {
        'exam_grades': exam_grades,
        'assignment_grades': assignment_grades,
        'role': getRole(request)
    }))
