from django import forms

from .models import GradableItem, Submission, ExamQuestion

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

class GradeAssignmentForm(forms.ModelForm):
	class Meta:
		model = Submission
		fields = ('score', 'grading_comment')

class ExamForm(forms.ModelForm):
	class Meta:
		model = GradableItem
		fields = ('max_score', 'title', 'description', 'due_date')
		exclude = ('type',)
	
class ExamQuestionForm(forms.ModelForm):
	class Meta:
		model = ExamQuestion
		fields = ('max_points', 'text')
	
