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

from .helpers import getRole
from .models import Announcement, Person

from os import listdir
from os.path import isfile, join

def logout(request):
	authLogout(request)
	return HttpResponseRedirect(reverse('base:index'))

def login(request):
	return render(request, 'users/login.html')

def auth(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	
	user = authenticate(username=username, password=password)

	if user is not None:
		authLogin(request, user)
		return HttpResponseRedirect(reverse('base:home'))

	else:
		return HttpResponseRedirect(reverse('base:invalidLogin'))

def invalidLogin(request):
	return render(request, 'users/invalidLogin.html')

def index(request):
	return login(request)

def home(request):
	# TODO
	announcments = Announcement.objects.all() 
	return render(request, 'home.html', {'announcements' : announcements, 'role' : getRole(request)})

def announcements(request):
	announcements = Announcement.objects.all() 
	return render(request, 'announcements.html', {'announcements' : announcements}) 

class CreateAnnouncementView(CreateView):
	template_name='base_form.html'
	model = Announcement
	fields = ['title', 'content']
	success_url = '/announcements'

	@method_decorator(login_required(login_url = '/'))
	def get(self, request):
		self.poster = Person.objects.get(user = request.user)
		return super(CreateAnnouncementView, self).get(self, request)
	
	@method_decorator(login_required(login_url = '/'))
	def post(self, request):
		self.poster = Person.objects.get(user = request.user)
		return super(CreateAnnouncementView, self).post(self, request)
		

	def form_valid(self, form):
		form.instance.poster = self.poster
		return super(CreateAnnouncementView, self).form_valid(form)
