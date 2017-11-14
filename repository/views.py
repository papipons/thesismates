import os, os.path
from django.conf import settings
from django.utils import timezone
import datetime
from django.utils.text import slugify
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


from django.http import HttpResponseForbidden, JsonResponse,  HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from django.contrib.auth.models import User
from admin_control.models import Course_Faculty_Assignment, Program
from . import models as repo_m
from . import forms as repo_f
from . import utils as repo_u
from . import tasks
from core import utils as core_u

from django.contrib.auth.decorators import (
	login_required
)
from django_ajax.decorators import ajax
from easy_pdf.rendering import render_to_pdf_response

# --------------------------------------------------------------------

@login_required(redirect_field_name=None)
def projects(request, project_status):
	context = {}
	template = 'repository/projects.html'
	context['search_form'] = repo_f.SearchForm()

	sem = repo_u.get_current_sem()
	ssy = repo_u.get_current_ssy()
	esy = repo_u.get_current_esy()

	is_admin = core_u.is_admin(request.user)
	is_faculty = core_u.is_faculty(request.user)
	is_student = core_u.is_student(request.user)
	is_coor = core_u.is_coor(request.user)
	is_adviser = core_u.is_adviser(request.user)

	if is_admin:
		context['is_admin'] = is_admin

	# PUBLISHED
	if project_status == "published":
		context['title'] = "Published Projects"
		projects = repo_m.Project.objects.filter(
			status = "published"
		)
		context['programs'] = Program.objects.all()

		if projects:
			context['projects'] = projects.order_by('-created_date')

	# ONGOING
	if project_status == "ongoing":
		context['title'] = "Ongoing Projects"
		projects = repo_m.Project.objects.exclude(status="published")

		if is_admin or is_coor:
			context['wide_events'] = repo_m.Event.objects.filter(posted_by=request.user, project_owner__status="ongoing")
			context['faculty'] = User.objects.filter(groups__name='faculty')
			context['add_project_form'] = repo_f.AddProjectForm()
			context['add_member_form'] = repo_f.AddMemberForm()
			context['aaa_form'] = repo_f.TermCourseForm()
			context['add_deadline_event_form'] = repo_f.AddDeadlineEvent(
					prefix = "add-deadline-event-form"
				)
			context['add_journal_event_form'] = repo_f.AddProgressEventForm(
					prefix = "add-journal-event-form"
				)

		if is_admin:
			courses = Course_Faculty_Assignment.objects.filter(
					assignment="coordinator",
					semester = sem,
					start_sy = ssy,
					end_sy = esy
				)
			available_advisers = repo_u.get_available_advisers(courses)
			context['courses'] = courses
			context['available_advisers'] = available_advisers

		elif is_faculty:
			if is_coor:
				assignment_coor = Course_Faculty_Assignment.objects.filter(
						faculty = request.user,
						assignment = "coordinator",
						semester = sem,
						start_sy = ssy,
						end_sy = esy
					)
				available_advisers = repo_u.get_available_advisers(assignment_coor)

				context['is_coor'] = is_coor
				context['available_advisers'] = available_advisers
				context['courses'] = assignment_coor

			if is_adviser:
				assignment_adviser = Course_Faculty_Assignment.objects.filter(
						faculty = request.user,
						assignment = "adviser",
						semester = sem,
						start_sy = ssy,
						end_sy = esy
					)

				advisoree_requests = repo_u.get_advisoree_requests(
						request.user, assignment_adviser
					)
				count = advisoree_requests.count()

				context['advisoree_requests'] = advisoree_requests
				context['requests_count'] = count
				context['is_adviser'] = is_adviser

		elif is_student:
			context['is_student'] = is_student

		if projects:
			context['projects'] = projects
			notifications = repo_u.get_notifications(projects, request.user)
			near_events = repo_u.get_near_events(projects)
			
			if notifications or near_events:
				count = 0

				if notifications:
					context['notifications'] = notifications.order_by('-created_date')
					count += notifications.count()
				if near_events:
					context['near_events'] = near_events.order_by('start_date')
					count += near_events.count()

				context['date_now'] = timezone.now()
				context['notif_count'] = count


		last_visit_record, created = repo_m.User_Last_Visit_Ongoing.objects.update_or_create(
				user = request.user,
				defaults = {'last_visit':timezone.now()}
			)

	context['project_status'] = project_status

	return render(request, template, context)

# --------------------------------------------------------------------

@login_required(redirect_field_name=None)
def project_profile(request, project_status, uid, slug):
	context = {}
	
	project = get_object_or_404(repo_m.Project, uid=uid, slug=slug)

	is_admin = core_u.is_admin(request.user)
	is_faculty = core_u.is_faculty(request.user)
	is_coor = core_u.is_coor(request.user, uid, slug)
	is_member = repo_u.user_is_member(request.user, uid, slug)
	is_adviser = core_u.is_adviser(request.user, uid, slug)
	allowed = repo_u.allowed_in_project(request.user, uid, slug)

	context['project_status'] = project_status
	context['project'] = project
	context['allowed'] = allowed

	if is_admin:
		context['is_admin'] = is_admin

	if is_coor:
		context['is_coor'] = is_coor

	if is_member:
		context['is_member'] = is_member

	# ONGOING
	if project_status == "ongoing" and project.status != "published":
		context['in_profile'] = True
		if project.status == "ongoing":
			if repo_u.allowed_in_project(request.user, uid, slug):

				context['edit_title_form'] = repo_f.EditTitleForm(instance=project)

				# MODAL
				context['add_deadline_event_form'] = repo_f.AddDeadlineEvent(
						prefix = "add-deadline-event-form"
					)
				context['add_journal_event_form'] = repo_f.AddProgressEventForm(
						prefix = "add-journal-event-form"
					)
				available_advisers = repo_u.get_available_advisers([project.coordinator])
				context['available_advisers'] = available_advisers
				context['members'] = project.members.all()


				semester = project.coordinator.semester
				start_sy = project.coordinator.start_sy
				end_sy = project.coordinator.end_sy
				

				if is_member:
					current_request = repo_m.Project_Adviser_Request.objects.filter(
							accepted=None,
							requester=project,
							requested__semester=semester,
							requested__start_sy=start_sy,
							requested__end_sy=end_sy
						)


					if current_request.count() != 0:
						current_obj = current_request.get()
						context['has_request'] = True
						context['current_request'] = current_request
						context['requested'] = "%s %s" % (
								current_obj.requested.faculty.first_name,
								current_obj.requested.faculty.last_name,
							)
					else:
						context['has_request'] = False

			response = render(
					request, 'repository/project_profile.html', context
				)

		# ONGOING PUB PROC STARTED
		else:
			context['status'] = project.status

			if project.status == "publication":
				context['add_file_form'] = repo_f.OfficialDocumentForm()

			context['files'] = repo_m.Document.objects.filter(
				owner__uid=uid,
				official = False
			)
			context['pre_final'] = repo_m.Document.objects.filter(
				owner__uid=uid,
				official = True
			)
			context['status'] = project.status

			response = render(
					request, 'repository/publication_process.html', context
				)

	# PUBLISHED
	elif project_status == "published" and project.status == "published":
		context['has_ongoing'] = repo_u.has_ongoing(request.user)
		response = render(
			request, 'repository/project_profile.html', context
		)

	# AFTER PUBLICATION
	elif project_status == "ongoing" and project.status == "published":
		return redirect(project_profile, project.status, uid, slug)

	# NOT FOUND
	else:
		# Return not found
		return HttpResponseNotFound()

	return response

# --------------------------------------------------------------------

@ajax
@login_required(redirect_field_name=None)
def profile(request, project_status, uid, slug):
	context = {}
	project = repo_m.Project.objects.get(uid=uid, slug=slug)
	members = project.members.all()
	is_coor = core_u.is_coor(request.user, uid, slug)
	is_admin = core_u.is_admin(request.user)
	context['is_member'] = repo_u.user_is_member(request.user, uid, slug)
	context['members'] = repo_m.Project_Membership.objects.filter(project__uid=uid)
	context['project'] = project
	context['project_status'] = project_status

	if is_coor or is_admin:
		context['is_coor'] = is_coor
		context['is_admin'] = is_admin
		context['non_members'] = User.objects.filter(
				groups__name='Students').exclude(
					id__in=[o.id for o in members]
			)

	if project.adviser != None:
		context['adviser'] = "%s %s" % (
				project.adviser.faculty.first_name, project.adviser.faculty.last_name 
			)

	context['coordinator'] = "%s %s" % (
			project.coordinator.faculty.first_name, project.coordinator.faculty.last_name 
		)
	
	context['abstract_form'] = repo_f.AbstractForm(
			initial={'abstract':project.abstract}
		)

	return render(request, 'repository/partials/project_profile.html', context)

# --------------------------------------------------------------------

@ajax
@login_required(redirect_field_name=None)
def calendar(request, project_status, uid, slug):
	context = {}
	project = get_object_or_404(repo_m.Project, uid=uid, slug=slug)
	allowed = repo_u.allowed_in_project(request.user, uid, slug)
	deadlines = repo_m.Event.objects.filter(
			Q(project_owner=project, event_type="deadline") | Q(course_owner=project.coordinator)
		)
	journals = repo_m.Event.objects.filter(
			Q(project_owner=project, event_type="journal")
		)

	if deadlines:
		context['deadlines'] = deadlines.order_by('start_date')

	if journals:
		context['journals'] = journals.order_by('start_date')

	if allowed:
		context['project_status'] = project_status
		context['allowed_in_project'] = allowed
	else:
		return HttpResponseForbidden()

	return render(request, 'repository/partials/project_calendar.html', context)

# --------------------------------------------------------------------

@ajax
@login_required(redirect_field_name=None)
def files(request, project_status, uid, slug):
	context = {}
	if repo_u.allowed_in_project(request.user, uid, slug):
		if core_u.is_admin(request.user):
			context['is_admin'] = True

		project = repo_m.Project.objects.get(uid=uid, slug=slug)
		context['project_status'] = project_status
		context['project'] = project
		context['files'] = repo_m.Document.objects.filter(owner__uid=uid)
		capacity = repo_u.get_working_files_capacity()
		context['capacity'] = capacity

		path = "%s/docpriv/%s" % (settings.MEDIA_ROOT, project.id)
		used_storage_size = repo_u.get_used_storage_size(path)
		context['used_storage_size'] = used_storage_size
		context['free_size'] = capacity - used_storage_size
		percentage = repo_u.get_percentage(used_storage_size)
		context['percentage'] = percentage
		context['add_file_form'] = repo_f.DocumentForm()

		if percentage >= 99.5:
			context['reached_cap'] = True
	else:
		return HttpResponseForbidden()

	return render(request, 'repository/partials/project_files.html', context)

# --------------------------------------------------------------------

@ajax
@login_required(redirect_field_name=None)
def log(request, project_status, uid, slug):
	context = {}
	if repo_u.allowed_in_project(request.user, uid, slug):
		sem = repo_u.get_current_sem()
		ssy = repo_u.get_current_ssy()
		esy = repo_u.get_current_esy()
		context['ssy'] = ssy
		context['esy'] = esy
		context['sem'] = sem
		project = repo_m.Project.objects.get(uid=uid, slug=slug)
		context['logs']	= repo_m.Project_Log.objects.filter(
			project_log=project, semester = sem, start_sy = ssy, end_sy = esy).order_by('-created_date')
	else:
		return HttpResponseForbidden()

	return render(request, 'repository/partials/project_log.html', context)

# --------------------------------------------------------------------

@login_required(redirect_field_name=None)
def get_events(request, project_status, uid, slug):
	project_uid = request.GET.get('projectUID')
	start = request.GET.get('start')
	end = request.GET.get('end')

	project_events = repo_u.get_project_events(
		project_uid, start, end, request.user
	)

	return JsonResponse(project_events, safe=False)

# --------------------------------------------------------------------

@ajax
@login_required(redirect_field_name=None)
def add_project(request, project_status):
	response = {}
	add_project_form = repo_f.AddProjectForm(request.POST)

	if add_project_form.is_valid():
		current_project = add_project_form.save_project()

		users = request.POST.getlist('users[]')
		if users:
			current_project_obj = repo_m.Project.objects.get(pk=current_project)

			for user in users:
				member_form = repo_f.AddMemberForm()
				member_form.save_members(user, current_project_obj, request.user)

		project = repo_m.Project.objects.get(pk=current_project)
		uid = project.uid
		slug = project.slug

		return redirect(project_profile, project_status, uid, slug)

	else:
		response['valid'] = False

	return response

# --------------------------------------------------------------------

@ajax
@login_required(redirect_field_name=None)
def add_event(request, project_status, uid = None, slug = None):
	event_type = request.POST.get('event_type')
	if uid == None and slug == None:
		course = request.POST.get('course')
		course_obj = Course_Faculty_Assignment.objects.get(pk=course)
		
		add_deadline_event_form = repo_f.AddDeadlineEvent(request.POST)

		if add_deadline_event_form.is_valid():
			add_deadline_event_form.save_event(
				request.user, None, event_type, course_obj
			)

	else:
		owner = repo_m.Project.objects.get(uid=uid)

		if event_type == "deadline":
			add_deadline_event_form = repo_f.AddDeadlineEvent(request.POST)

			if add_deadline_event_form.is_valid():
				add_deadline_event_form.save_event(
					request.user, owner, event_type
				)

		elif event_type == "journal":
			add_progress_event_form = repo_f.AddProgressEventForm(request.POST)
			members = request.POST.getlist('included_members[]')
			if add_progress_event_form.is_valid():
				add_progress_event_form.save_event(
					request.user, owner, event_type, members
				)

# --------------------------------------------------------------------

@ajax
@login_required(redirect_field_name=None)
def save_event_changes(request, project_status, uid, slug):
	event_id = request.POST.get('id')
	start = request.POST.get('start')
	end = request.POST.get('end')

	event = repo_m.Event.objects.filter(pk=event_id)
	event.update(start_date=start)
	event.update(end_date=end)

# --------------------------------------------------------------------

@ajax
@login_required(redirect_field_name=None)
def remove_event(request, project_status, uid, slug):
	event_id = request.POST.get('id')
	event = repo_m.Event.objects.get(pk=event_id)
	project = repo_m.Project.objects.get(uid=uid, slug=slug)

	repo_u.add_project_log(
		project,
		"deleted the event: %s" % (event.title),
		request.user
	)

	event.delete()

# --------------------------------------------------------------------

@login_required(redirect_field_name=None)
def upload_file(request, project_status, uid, slug):
	project = repo_m.Project.objects.get(uid=uid, slug=slug)

	response = {}
	response_files = []

	if project.status == "ongoing":
		official = False
	else:
		official = True

	if project.status == "publication":
		form = repo_f.OfficialDocumentForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['docfile']
			newdoc = repo_u.save_file(file, project, request.user, official)

			temp = {}
			temp['id'] = str(newdoc.id) 
			temp['name'] = str(newdoc.filename())
			temp['uploaded_by'] = str(newdoc.uploaded_by)

			response_files.append(temp)

			response['url'] = "/projects/%s/%s/%s" % (
				project_status, uid, slug
			)
			response['files'] = response_files
			response['valid'] = True
		else:
			response['valid'] = False
	else:
		form = repo_f.DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			path = "%s/docpriv/%s" % (settings.MEDIA_ROOT, project.id)

			files = form.cleaned_data['docfile']
			space_is_sufficient = repo_u.check_if_sufficient(path, files)

			if space_is_sufficient:
				for file in files:
					newdoc = repo_u.save_file(
						file, project, 
						request.user, official)

				response['valid'] = True
			else:
				response['valid'] = False

		else:
			response['valid'] = False


	return JsonResponse(response, safe=False)

# --------------------------------------------------------------------

@ajax
def delete_file(request, project_status, uid, slug, fileid):
	response = {}
	deleted = repo_u.delete_file(request.user, uid, slug, fileid)

	if deleted == "existent":
		project = repo_m.Project.objects.get(uid=uid, slug=slug)
		path = "%s/docpriv/%s" % (settings.MEDIA_ROOT, project.id)
		used_storage_size = repo_u.get_used_storage_size(path)
		percentage = repo_u.get_percentage(used_storage_size)

		response['fileid'] = fileid
		response['percentage'] = percentage
		response['used_storage_size'] = used_storage_size
	elif deleted == "inexistent":
		response = HttpResponseNotFound()
	elif deleted == "forbidden":
		response = HttpResponseForbidden()

	return response

# --------------------------------------------------------------------

@login_required(redirect_field_name=None)
def download_file(request, project_status, uid, slug, fileid):
	response = repo_u.serve_file(
		request.user,
		uid, slug, fileid,
		'download'
	)

	return response

# --------------------------------------------------------------------

@login_required(redirect_field_name=None)
def view_file(request, project_status, uid, slug, fileid):
	response = repo_u.serve_file(
		request.user,
		uid, slug, fileid,
		'view'
	)

	return response

# --------------------------------------------------------------------

@ajax
def doc_req(request, project_status, uid, slug):
	project = get_object_or_404(repo_m.Project, uid=uid, slug=slug)
	sem = repo_u.get_current_sem()
	ssy = repo_u.get_current_ssy()
	esy = repo_u.get_current_esy()

	req, created = repo_m.User_Docu_Request.objects.update_or_create(
			user = request.user,
			req_docs = project,
			semester = sem,
			start_sy = ssy,
			end_sy = esy,
			defaults = {'access':None}
		)

# --------------------------------------------------------------------

@ajax
@login_required(redirect_field_name=None)
def view_documentation(request, project_status, uid, slug):
	context = {}

	if request.user.is_authenticated() and repo_u.has_ongoing(request.user) or core_u.is_admin(request.user):
		# project = get_object_or_404(repo_m.Project, uid=uid, slug=slug)
		# sem = repo_u.get_current_sem()
		# ssy = repo_u.get_current_ssy()
		# esy = repo_u.get_current_esy()

		# try:
		#     req_doc  = repo_m.User_Docu_Request.objects.filter(
		# 		user = request.user,
		# 		req_docs = project,
		# 		semester = sem,
		# 		start_sy = ssy,
		# 		end_sy = esy)

		#     context['has_request'] = True

		#     if req_doc.get().access == True:
		#     	context['has_access'] = True

		#     if req_doc.get().access == False:
		#     	context['has_access'] = False

		#     if req_doc.get().access == None:
		#     	context['has_access'] = "unknown"
		# except ObjectDoesNotExist:
		#     context['has_request'] = False

		path = "%s/public/image_docs/%s" % (settings.MEDIA_ROOT,uid)
		num_files = len([f for f in os.listdir(path)
		                if os.path.isfile(os.path.join(path, f))])

		urls = []
		for x in range(num_files):
			url = "/media/public/image_docs/%s/%s.png" %(uid, x)
			urls.append(url)

		context['urls'] = urls

		return render(request, 'repository/view_file.html', context)
	else:
		return HttpResponseForbidden()

# --------------------------------------------------------------------

@ajax
@login_required(redirect_field_name=None)
def add_member(request, project_status, uid, slug):
	response = {}

	user = request.POST.get('user')
	if user:
		project = repo_m.Project.objects.get(
			uid = uid,
			slug = slug
		)

		member_form = repo_f.AddMemberForm()
		to_add = member_form.save_members(user, project, request.user)

		response['valid'] = True
		response['id'] = to_add.id
		response['full_name'] = "%s %s" % (to_add.first_name, to_add.last_name)

	else:
		response['valid'] = False

	return response

# --------------------------------------------------------------------

@login_required(redirect_field_name=None)
def generate_report(request, project_status):
	program = request.POST.get('program')
	if core_u.is_admin(request.user):
		context = {}
		if program == "all":
			projects = repo_m.Project.objects.filter(status="published")
		else:
			projects = repo_m.Project.objects.filter(status="published", coordinator__course__program=program)
		context['projects'] = projects
		context['date'] = timezone.now()

		return render_to_pdf_response(request, 'repository/generate_report.html', context)
	else:
		return HttpResponseForbidden()

# --------------------------------------------------------------------

# @ajax
@login_required(redirect_field_name=None)
def generate_journal(request, project_status, uid, slug):
	context = {}

	start = request.GET.get('add-journal-event-form-start_date')
	end = request.GET.get('add-journal-event-form-end_date')

	context['journals'] = repo_u.get_journal_events(uid, start, end)
	context['start'] = start
	context['end'] = end

	project = repo_m.Project.objects.get(uid=uid, slug=slug)

	if project.adviser is not None:
		context['adviser'] = project.adviser.faculty

	repo_u.add_project_log(
		project,
		"generated a journal",
		request.user
	)

	return render_to_pdf_response(request, 'repository/journal.html', context)

# --------------------------------------------------------------------

@ajax
def assign_advisers(request, project_status):
	response = {}
	course = request.POST.get('course')
	adviser = request.POST.get('faculty')
	add_assignment_form = repo_f.TermCourseForm(request.POST)

	if add_assignment_form.is_valid():
		response = add_assignment_form.save_assignment(course, adviser)
	else:
		response['valid'] = False
		response['errors'] = "Please fill up all the fields."

	return response

# --------------------------------------------------------------------

@ajax
def rejection(request, project_status, uid, slug):
	project = repo_m.Project.objects.filter(uid=uid, slug=slug)
	repo_u.change_status(project, "publication")
	return redirect(project_profile, project_status, uid, slug)

# --------------------------------------------------------------------

@ajax
def start_publication(request, project_status, uid, slug):
	repo_u.start_publication(request.user, uid, slug)
	return redirect(project_profile, project_status, uid, slug)

# --------------------------------------------------------------------

@ajax
def start_confirmation(request, project_status, uid, slug):
	repo_u.start_confirmation(request.user, uid, slug)
	return redirect(project_profile, project_status, uid, slug)

# --------------------------------------------------------------------

@ajax
def start_processing(request, project_status, uid, slug):
	repo_u.start_processing(request.user, uid, slug)
	return redirect(project_profile, project_status, uid, slug)

# --------------------------------------------------------------------

@ajax
def get_search(request, project_status):
	form = repo_f.SearchForm(request.POST)
	context = {}
	context['project_status'] = project_status
	if form.is_valid():
		context['projects'] = repo_u.get_search(form, project_status, request.user).order_by('-created_date')
		words = request.POST.get('search')
		keywords = words.split()
		context['keywords'] = keywords

		return render(request, 'repository/partials/search.html', context)

# --------------------------------------------------------------------

@ajax
def edit_abstract(request, project_status, uid, slug):
	form = repo_f.AbstractForm(request.POST)
	response = {}
	project = repo_m.Project.objects.filter(uid=uid, slug=slug)
	if form.is_valid():
		new_abstract = form.update_abstract(project, request.user)
		response['valid'] = True
		response['new_abstract'] = new_abstract

	else:
		response['valid'] = False
		response['error'] = "Could not save abstract with no content"

	return response

# --------------------------------------------------------------------

@ajax
def get_user_for_delete(request, project_status, uid, slug):
	id = request.POST.get('id')
	to_return = {}

	if bool(id):
		to_delete = repo_m.Project_Membership.objects.get(pk=id)

		if to_delete.member == request.user:
			response = "Are you sure you want to leave?"
		else:
			response = "Remove %s %s?" % (to_delete.member.first_name, to_delete.member.last_name)
	else:
		response = False

	to_return['message'] = response

	return to_return

# --------------------------------------------------------------------

@ajax
def leave_group(request, project_status, uid, slug):
	to_delete = request.POST.get('id')
	project = repo_m.Project.objects.get(uid=uid, slug=slug)

	coor = repo_u.leave_group(project, to_delete, request.user)

	if not coor:
		return redirect(projects, "ongoing")

# --------------------------------------------------------------------

@ajax
def request_adviser(request, project_status, uid, slug):
	faculty = request.POST.get('faculty')
	if faculty:
		project = repo_m.Project.objects.get(uid=uid, slug=slug)
		assignment = Course_Faculty_Assignment.objects.get(pk=faculty)

		adviser_request = repo_m.Project_Adviser_Request()
		adviser_request.requester = project
		adviser_request.requested = assignment
		adviser_request.accepted = None
		adviser_request.save()

		adviser = "%s %s" % (assignment.faculty.first_name, assignment.faculty.last_name)

		repo_u.add_project_log(
			project,
			"requested %s to be the project adviser" % adviser,
			request.user
		)

		return redirect(project_profile, project_status, uid, slug)

# --------------------------------------------------------------------

def respond_advisoree_request(request, project_status, uid, slug, response):
	project = repo_m.Project.objects.filter(uid=uid, slug=slug)
	project_object = project.get()
	assignment = Course_Faculty_Assignment.objects.filter(
			faculty = request.user, assignment="adviser",
			course = project_object.coordinator.course
		)

	advisoree_request = repo_m.Project_Adviser_Request.objects.filter(
			requester = project, requested = assignment
		)

	log = repo_m.Project_Log()
	log.project_log = project.get()
	log.actor = request.user

	if response == "accepted":
		advisoree_request.update(accepted=True)
		project.update(adviser=assignment.get())

		log.message = "accepted adviser request"
		log.save()
		
		return redirect(project_profile, "ongoing", project_object.uid, project_object.slug)

	if response == "rejected":
		advisoree_request.update(accepted=False)

		log.message = "rejected adviser request"
		log.save()

		return redirect(projects, "ongoing")

# --------------------------------------------------------------------

@ajax
def edit_title(request, project_status, uid, slug):
	project = repo_m.Project.objects.filter(uid=uid, slug=slug)
	form = repo_f.EditTitleForm(request.POST, instance=project.get())

	if project.get().status == "ongoing":
		if form.is_valid():
			new_title = form.cleaned_data['title']
			new_slug = slugify(new_title)

			repo_u.add_project_log(
				project.get(),
				"changed project title to: %s" % new_title,
				request.user
			)

			project.update(title=new_title, slug=new_slug)

			return redirect(project_profile, "ongoing", uid, new_slug)
		else:
			response = {}
			response['error'] = "Title is already taken"

			return response
	else:
		return HttpResponseForbidden()

# --------------------------------------------------------------------

@ajax
def get_event_instance(request, project_status, uid, slug):
	id = request.POST.get('id')
	context = {}
	event = repo_m.Event.objects.get(pk=id)
	start_date = datetime.datetime.strftime(event.start_date, '%B %d, %Y')

	context['event'] = event
	context['add_deadline_event_form'] = repo_f.AddDeadlineEvent(
			instance = event,
			prefix = "edit-deadline-event-form",
			initial={
				'start_date': start_date,
				'start_time': event.start_time,
				'notes':event.notes
			}
		)
	context['add_journal_event_form'] = repo_f.AddProgressEventForm(
			instance = event,
			prefix = "edit-journal-event-form",
			initial = {
				'start_date': start_date
			}
		)

	project = event.project_owner
	if project:
		context['members'] = project.members.all()


	return render(request, 'repository/edit_event_form.html', context)

# --------------------------------------------------------------------

@ajax
def save_manual(request, project_status, uid, slug):
	id = request.POST.get('id')
	event = repo_m.Event.objects.get(pk=id)

	if event.event_type == "deadline":
		form = repo_f.AddDeadlineEvent(request.POST, instance=event)
		if form.is_valid():
			form.update()
	else:
		members = request.POST.getlist('included_members[]')
		form = repo_f.AddProgressEventForm(request.POST, instance=event)
		if form.is_valid():
			form.update(members, event)
		








