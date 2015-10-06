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
from .models import GradableItem

from os import listdir
from os.path import isfile, join

def assignments(request):
	assignments = GradableItem.objects.filter(type='HMWK')
	return render(request, 'grades/assignments.html', {'assignments' : assignments})

class CreateAssignmentView(CreateView):
	template_name='base_form.html'
	model = GradableItem 
	fields = ['max_score', 'title', 'description', 'due_date']
	success_url = '/assignments'

	def form_valid(self, form):
		form.instance.type = "HMWK"
		return super(CreateAssignmentView, self).form_valid(form)
