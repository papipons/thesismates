from django.shortcuts import render, redirect
from django.contrib.auth.views import login, logout
from django.contrib.auth.models import User
from repository.models import Project_Membership, Project
from admin_control.models import Course_Faculty_Assignment
from .forms import SignUpForm, AccountManagementForm, NewPassForm
from repository.views import project_profile, projects
from repository import utils as repo_u
from core import utils as core_u
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import (
	login_required
)

# --------------------------------------------------------------------

def index(request):
	context = {}

	if request.user.is_authenticated():
		return redirect(projects, "ongoing")

	else:
		return login(
				request, 
				template_name = 'core/landing.html', 
				extra_context = context
			)

# --------------------------------------------------------------------

@login_required(redirect_field_name=None)
def log_out(request):
	logout(request)
	return redirect(index)

# --------------------------------------------------------------------

def sign_up(request):
	context = {}

	# if request.user.is_authenticated:
	# 	return redirect(index)

	if request.method == 'GET':
		context['signup_form'] = SignUpForm()
	if request.method == 'POST':
		signup_form = SignUpForm(request.POST)

		if signup_form.is_valid():
			user = signup_form.save_membership()

			login(request,user)

			return redirect('/')
		else:
			context['signup_form'] = signup_form


	return render(request, 'core/sign_up.html', context)

# --------------------------------------------------------------------

@login_required(redirect_field_name=None)
def account(request):
	context = {}
	context['user'] = request.user
	is_admin = core_u.is_admin(request.user)
	context['is_admin'] = is_admin

	if request.method == "POST":

		if "submit-account-management" in request.POST:
			form = AccountManagementForm(request.POST, instance=request.user)

			if form.is_valid():
				form.save()
				context['success_account_management'] = True

			new_pass_form = NewPassForm(request.user)

		if "submit-new-pass" in request.POST:
			new_pass_form = NewPassForm(request.user, request.POST, instance=request.user)

			if new_pass_form.is_valid():
				new_pass_form.update_password()
				update_session_auth_hash(request, new_pass_form.user)
				context['success_pass'] = True

			form = AccountManagementForm(instance=request.user)

	if request.method == 'GET':
		form = AccountManagementForm(instance=request.user)
		new_pass_form = NewPassForm(request.user)

	context['pass'] = new_pass_form
	context['account_management'] = form
	context['account'] = True
	return render(request, 'core/account.html', context)


