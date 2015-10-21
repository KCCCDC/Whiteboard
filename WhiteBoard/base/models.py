from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    # TA, ADMN, PROF, or STUD
    type = models.CharField(max_length=4)
    user = models.ForeignKey(User)


class Announcement(models.Model):
    poster = models.ForeignKey(Person)
    date_posted = models.DateField(auto_now=False, auto_now_add=True)
    content = models.CharField(max_length=300)
    title = models.CharField(max_length=50)

    class Meta:
        ordering = ['-date_posted']
