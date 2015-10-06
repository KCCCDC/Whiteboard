from django.db import models
from django.contrib.auth.models import User

from WhiteBoard.base.models import Person

def getUploadDir(instance, filename):
	return "static/" + filename

class GradableItem(models.Model):
	type = models.CharField(max_length=16)
	max_score = models.IntegerField()
	title = models.CharField(max_length=64)
	description = models.CharField(max_length=512, blank=True)
	due_date = models.DateField(auto_now=False, auto_now_add=False)
	file = models.FileField(upload_to=getUploadDir, blank=True, null=True)

class Submission(models.Model):
	gradableItem = models.ForeignKey(GradableItem)
	submitter = models.ForeignKey(Person, related_name='submission_submitter')
	date_submitted = models.DateField(auto_now=False, auto_now_add=True)
	grader = models.ForeignKey(Person, related_name='submission_grader', null=True)
	score = models.IntegerField(null=True)
	submission_text = models.CharField(max_length=512, blank=True)
	grading_comment = models.CharField(max_length=256, blank=True, null=True)
	file = models.FileField(blank=True, null=True)

