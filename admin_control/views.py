from django.shortcuts import render
from django.contrib.auth.models import User
from django_ajax.decorators import ajax
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import (
	user_passes_test
)

from . import models as adcon_m
from . import forms as adcon_f
from . import utils
from core import utils as core_u

# --------------------------------------------------------------------

def manage(request):
	if core_u.is_admin(request.user) == True:
		context = {}
		context['is_admin'] = True
		context['manage'] = True

		return render(request, 'admin_control/manage.html', context)
	else:
		return HttpResponseForbidden()

# --------------------------------------------------------------------

@ajax
def courses(request):
	context = {}

	courses_list = adcon_m.Course.objects.all()

	context['courses'] = courses_list
	context['form'] = adcon_f.CourseForm()

	return render(request, 'admin_control/partials/courses.html',context)

# --------------------------------------------------------------------

@ajax
def programs(request):
	context = {}
	context['form'] = adcon_f.ProgramForm()
	context['programs'] = adcon_m.Program.objects.all()

	return render(request, 'admin_control/partials/programs.html', context)

# --------------------------------------------------------------------

@ajax
def add_program(request):
	response = {}
	form = adcon_f.ProgramForm(request.POST)

	if form.is_valid():
		form.save()
		response['valid'] = True
	else:
		response['valid'] = False
		response['errors'] = form.errors

	return response

# --------------------------------------------------------------------

@ajax
def add_course(request):
	response = {}
	course_form = adcon_f.CourseForm(request.POST)

	if course_form.is_valid():
		object = course_form.save()
		response['code'] = object.program.code
		response['valid'] = True
	else:
		response['valid'] = False
		response['errors'] = course_form.errors

	return response

# --------------------------------------------------------------------

@ajax
def edit_program(request):
	orig = request.POST.get('originalName')
	name = request.POST.get('name')
	code = request.POST.get('code')
	desc = request.POST.get('desc')

	adcon_m.Program.objects.filter(name=orig).update(
		code = code,
		name = name,
		description = desc
	)

	print "PASOK"

# --------------------------------------------------------------------

@ajax
def edit_course(request):
	new_name = request.POST.get('newName')
	original_name = request.POST.get('originalName')

	edited = adcon_m.Course.objects.filter(name=original_name).update(name=new_name)

# --------------------------------------------------------------------

@ajax
def settings(request):
	context = {}
	admin_settings = adcon_m.Setting.objects.all()

	current_start_sy = admin_settings.get(name="start_school_year").value
	current_end_sy = admin_settings.get(name="end_school_year").value
	current_sem = admin_settings.get(name="semester").value
	current_capacity = admin_settings.get(
		name="working_files_capacity").value

	sy = "%s - %s" % (current_start_sy, current_end_sy)

	context['sem_form'] = adcon_f.SemForm(
			initial ={'value': current_sem},
			prefix = "sem-form"
		)
	context['sy_form'] = adcon_f.SyForm(
			initial ={'value': sy},
			prefix = "sy-form"
		)

	context['capacity_form'] = adcon_f.CapacityForm(
			initial={'value': current_capacity},
			prefix = "capacity-form"
		)

	return render(request,'admin_control/partials/settings.html',context)

# --------------------------------------------------------------------

@ajax
def save_settings(request):
	sem = request.POST.get('sem')
	sy = request.POST.get('sy')
	capacity = request.POST.get('capacity')

	sy = sy.replace('-', ' ').split(' ')

	sem_to_update = adcon_m.Setting.objects.filter(name="semester")
	sem_to_update.update(value=sem)

	start_sy_to_update = adcon_m.Setting.objects.filter(name="start_school_year")
	start_sy_to_update.update(value=sy[0])

	end_sy_to_update = adcon_m.Setting.objects.filter(name="end_school_year")
	end_sy_to_update.update(value=sy[1])

	capacity_to_update = adcon_m.Setting.objects.filter(name="working_files_capacity")
	capacity_to_update.update(value=capacity)

# --------------------------------------------------------------------

@ajax
def assignments(request):
	context = {}
	
	context['assignments'] = adcon_m.Course_Faculty_Assignment.objects.all()
	context['form'] = adcon_f.TermCourseForm()
	context['faculty'] = User.objects.filter(groups__name='faculty')

	return render(request,'admin_control/partials/assignments.html',context)

# --------------------------------------------------------------------

@ajax
def add_assignment(request):
	response = {}
	course = request.POST.get('course')
	coordinator = request.POST.get('faculty')
	add_assignment_form = adcon_f.TermCourseForm(request.POST)

	if add_assignment_form.is_valid():
		response = add_assignment_form.save_assignment(course, coordinator)
	else:
		response['valid'] = False
		response['errors'] = "Please fill up all the fields."

	return response

# --------------------------------------------------------------------

@ajax
def users(request):
	context = {}

	context['users'] = User.objects.exclude(username="master")
	context['form'] = adcon_f.AdminAddUserForm()

	return render(request, 'admin_control/partials/users.html', context)

# --------------------------------------------------------------------

@ajax
def add_user(request):
	email = request.POST.get('email')
	return utils.create_user_send_invite(email)

