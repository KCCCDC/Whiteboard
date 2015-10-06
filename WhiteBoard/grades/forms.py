from django import forms

from .models import GradableItem, Submission

class AssignmentForm(forms.ModelForm):
	class Meta:
		model = GradableItem
		fields = ('max_score', 'title', 'description', 'due_date', 'file')
		exclude = ('type',)

class SubmissionForm(forms.ModelForm):
	class Meta:
		model = Submission
		fields = ('submission_text', 'file')
		exclude = ('gradableItem', 'submitter', 'date_submitted', 'grader', 'score', 'grading_comment')
