from django.contrib.auth.models import User
from repository import models as repo_m
from admin_control.models import Course_Faculty_Assignment, Setting

# --------------------------------------------------------------------

def is_coor(user, uid = None, slug = None):
	ssy = Setting.objects.get(name="start_school_year").value
	esy = Setting.objects.get(name="end_school_year").value
	sem = Setting.objects.get(name="semester").value

	if uid and slug:
		if repo_m.Project.objects.filter(
			uid = uid, 
			slug = slug, 
			coordinator__faculty = user).exists():
			return True

		else:
			return False
	else:
		if Course_Faculty_Assignment.objects.filter(
			faculty=user, assignment="coordinator",
			start_sy = ssy,
			end_sy = esy,
			semester = sem):
			return True
		else:
			return False

# --------------------------------------------------------------------

def is_adviser(user, uid = None, slug = None):
	ssy = Setting.objects.get(name="start_school_year").value
	esy = Setting.objects.get(name="end_school_year").value
	sem = Setting.objects.get(name="semester").value

	if uid and slug:
		project = repo_m.Project.objects.get(uid=uid, slug=slug)

		if project.adviser == None:
			return False
		else:
			adviser = project.adviser.faculty

			if adviser == user:
				return True
			else:
				return False
	else:
		if Course_Faculty_Assignment.objects.filter(
			faculty=user, assignment="adviser",
			start_sy = ssy,
			end_sy = esy,
			semester = sem):
			return True
		else:
			return False

# --------------------------------------------------------------------

def is_faculty(user):
	if user.groups.filter(name="faculty").exists():
		return True
	else:
		return False

# --------------------------------------------------------------------

def is_student(user):
	if user.groups.filter(name="students").exists():
		return True
	else:
		return False

# --------------------------------------------------------------------

def is_admin(user):
	if user.groups.filter(name="admin").exists():
		return True
	else:
		return False
