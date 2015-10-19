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
from django.views.decorators.csrf import csrf_exempt

from WhiteBoard.base.models import Person
from WhiteBoard.grades.models import GradableItem
from .forms import EventForm
from .models import Event
from WhiteBoard.base.helpers import getRole

from os import listdir
from os.path import isfile, join

def calendar(request):
    gradable_items = GradableItem.objects.all().order_by('due_date')
    events = Event.objects.all().order_by('date')
    return render(request, "calendar/calendar.html", {'gradable_items' : gradable_items, 'events' : events})

@csrf_exempt
def edit_event(request):
    if request.method == "GET":
        if 'event' not in request.method:
            form = EventForm()
        else:
            event = Event.objects.get(id=request.GET['event'])
            form = EventForm(instance=instance)
        return render(request, "base_form.html", {'form' : form })
    elif request.method == "POST":
        if 'event' not in request.GET:
            form = EventForm(request.POST)
        else:
            instance = Event.objects.get(id=request.GET['event'])
            form = EventForm(request.POST, instance=instance)
        form.save()
        return HttpResponseRedirect(reverse("calendar:calendar"))
