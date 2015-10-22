from django.contrib import admin
from .models import (GradableItem, Submission, ExamSubmission,
     ExamQuestion, ExamAnswer)

admin.site.register(GradableItem)
admin.site.register(Submission)
admin.site.register(ExamSubmission)
admin.site.register(ExamQuestion)
admin.site.register(ExamAnswer)
