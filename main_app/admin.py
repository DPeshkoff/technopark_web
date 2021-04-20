from django.contrib import admin
from main_app import models

admin.site.register(models.UserProfile)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.QuestionVote)
admin.site.register(models.AnswerVote)
admin.site.register(models.Tag)