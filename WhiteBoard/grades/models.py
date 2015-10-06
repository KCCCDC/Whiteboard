from django.db import models
from django.contrib.auth.models import User

from WhiteBoard.base.models import Person

class GradableItem(models.Model):
	type = models.CharField(max_length=16)
	max_score = models.IntegerField()
	title = models.CharField(max_length=64)
	description = models.CharField(max_length=512)
	due_date = models.DateField(auto_now=False, auto_now_add=False)
	# TODO - add file(s) 

class Submission(models.Model):
	gradableItem = models.ForeignKey(GradableItem)
	submitter = models.ForeignKey(Person, related_name='submission_submitter')
	date_submitted = models.DateField(auto_now=False, auto_now_add=True)
	grader = models.ForeignKey(Person, related_name='submission_grader')
	score = models.IntegerField()
	submission_text = models.CharField(max_length=512)
	grading_comment = models.CharField(max_length=256)
	# TODO - add File

