from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User

# --------------------------------------------------------------------

class Program(models.Model):
	# Attributes
	code         = models.CharField(max_length=50, unique=True)
	name         = models.CharField(max_length=50, unique=True)
	description  = models.CharField(max_length=255)
	created_date = models.DateTimeField(default=timezone.now)

	# Methods
	def __unicode__(self):
	    return self.name

# --------------------------------------------------------------------

class Course(models.Model):
	# Attributes
	name         = models.CharField(max_length=255)
	created_date = models.DateTimeField(default=timezone.now)

	# Relations
	program = models.ForeignKey(Program, related_name='program')

	# Methods
	def __unicode__(self):
	    return self.name

	class Meta:
		ordering = ('name',)


# --------------------------------------------------------------------

class Setting(models.Model):
	# Attributes
	name  = models.CharField(max_length=50)
	value = models.CharField(max_length=50)

	# Methods
	def __unicode__(self):
		return self.value

# --------------------------------------------------------------------

class Course_Faculty_Assignment(models.Model):
	# Attributes
	semester   = models.CharField(max_length=50)
	start_sy   = models.CharField(max_length=50)
	end_sy     = models.CharField(max_length=50)
	assignment = models.CharField(max_length=255)

	# Relations
	course  = models.ForeignKey(Course, related_name="course")
	faculty = models.ForeignKey(User, related_name="faculty")

	# Methods
	def __unicode__(self):
		return self.course.name

# --------------------------------------------------------------------

admin.site.register(Course)
admin.site.register(Program)
admin.site.register(Setting)
admin.site.register(Course_Faculty_Assignment)
