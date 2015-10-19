from django.db import models
from django.contrib.auth.models import User

from WhiteBoard.base.models import Person
from WhiteBoard.grades.models import GradableItem

class Event(models.Model):
    title = models.CharField(max_length=32)
    date = models.DateField(auto_now=False, auto_now_add=False)
    description = models.CharField(max_length=256)
