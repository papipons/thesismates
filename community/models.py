from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User

# --------------------------------------------------------------------

class Question(models.Model):
	# Attributes
	title        = models.CharField(max_length=255, unique=True)
	description  = models.TextField(blank=True, null=True)
	created_date = models.DateTimeField(default=timezone.now)
	slug         = models.SlugField()
	accepted = models.NullBooleanField(null=True)

	# Relations
	asked_by = models.ForeignKey(User, related_name="asked_by")

	# Methods
	def __unicode__(self):
	    return self.title

# --------------------------------------------------------------------

class Question_Answer(models.Model):
	# Attributes
	answer       = models.TextField(blank=True, null=True)
	created_date = models.DateTimeField(default=timezone.now)
	accepted = models.NullBooleanField(null=True)

	# Relations
	question    = models.ForeignKey(Question, related_name="question")
	answered_by = models.ForeignKey(User, related_name="answered_by")

	# Methods
	def __unicode__(self):
	    return self.answer

# --------------------------------------------------------------------

admin.site.register(Question)
admin.site.register(Question_Answer)

