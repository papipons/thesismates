import datetime
from django.utils import timezone
import pytz
from django.core.servers.basehttp import FileWrapper
import os
import operator
from bitmath import *

from django.shortcuts import get_object_or_404

from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponseForbidden,HttpResponse

from django.db.models import Q
from django.contrib.auth.models import User
from admin_control.models import Course_Faculty_Assignment, Setting
from . import models as repo_m
from . import tasks
from core import utils as core_u

from django.utils.crypto import get_random_string

# --------------------------------------------------------------------

def create_secret_code():
	valid = False

	while valid == False:
		rand_string = get_random_string(length=8)
		secret_code = str(rand_string).upper()

		if not repo_m.Project.objects.filter(
			secret_code = secret_code).exists():
			valid = True

	return secret_code

# --------------------------------------------------------------------

def get_project_events(project_owner, start, end, current_user):
	events = []

	start_object = datetime.datetime.strptime(start,'%Y-%m-%d')
	end_object = datetime.datetime.strptime(end,'%Y-%m-%d')

	project = repo_m.Project.objects.get(uid=project_owner)

	project_events = repo_m.Event.objects.filter(
			Q(project_owner__uid=project_owner, start_date__gte=start_object) | Q(course_owner=project.coordinator)
		)

	for event in project_events:
		temp = {}
		posted_by = "%s %s" % (event.posted_by.first_name, event.posted_by.last_name)
		temp['posted_by'] = posted_by
		temp['type'] = event.event_type
		if event.event_type == "deadline":
			temp['id'] = event.id
			temp['title'] = event.title
			temp['color'] = "#e74c3c" # Red
			temp['notes'] = event.notes

			end = event.start_date + datetime.timedelta(days=1)
			temp['end'] = "%s" % (end)

			if event.start_time is None:
				temp['start'] = event.start_date
				temp['durationEditable'] = False
			else:
				temp['start'] = "%sT%s" % (event.start_date, event.start_time)

		elif event.event_type == "journal":
			temp['id'] = event.id
			temp['title'] = event.title
			temp['notes'] = event.notes
			temp['durationEditable'] = False
			temp['color'] = "#2ecc71" # Green
			temp['start'] = event.start_date
			temp['end'] = event.end_date

			members = []
			for member in event.included_members.all():
				name = "%s %s" % (member.first_name, member.last_name)
				members.append(name)

			print members
			temp['members'] = members

		if project_is_ongoing(project.uid, project.slug) == True:
			if event.posted_by == current_user:
				temp['editable'] = True
		else:
			temp['editable'] = False

		events.append(temp)

	return events

# --------------------------------------------------------------------

def get_ongoing_projects(user):
	ongoing_projects = None

	if core_u.is_admin(user) == True:
		ongoing_projects = repo_m.Project.objects.exclude(status="published")

	if core_u.is_student(user) == True:
		ongoing_projects = user.project_set.all().filter(
			~Q(status="published")
		)

	if core_u.is_coor(user) == True and core_u.is_adviser(user) == True:
		ongoing_projects = repo_m.Project.objects.filter(
			Q(adviser__faculty=user) | Q(coordinator__faculty=user),
			Q(status="ongoing") | Q(status="publication") |
			Q(status="processing") | Q(status="confirmation")
		)

		if ongoing_projects:
			return ongoing_projects.order_by('-created_date')
		else:
			return None

	if core_u.is_coor(user) == True:
		ongoing_projects = repo_m.Project.objects.filter(
			Q(coordinator__faculty=user),
			Q(status="ongoing") | Q(status="publication") |
			Q(status="processing") | Q(status="confirmation")
		)
	if core_u.is_adviser(user) == True:
		ongoing_projects = repo_m.Project.objects.filter(
			Q(adviser__faculty=user),
			Q(status="ongoing") | Q(status="publication") |
			Q(status="processing") | Q(status="confirmation")
		)

	if ongoing_projects:
		return ongoing_projects.order_by('-created_date')
	else:
		return None

# --------------------------------------------------------------------

def user_is_member(user, uid, slug):
	project = repo_m.Project.objects.get(uid=uid, slug=slug)
	if repo_m.Project_Membership.objects.filter(
		project=project, member=user).exists():
		return True
	else:
		return False

# --------------------------------------------------------------------

def project_is_ongoing(uid, slug):
	project = repo_m.Project.objects.get(uid=uid, slug=slug)
	if project.status == "ongoing":
		return True
	else:
		return False

# --------------------------------------------------------------------

def project_is_processing(uid, slug):
	project = repo_m.Project.objects.get(uid=uid, slug=slug)
	if project.status == "processing":
		return True
	else:
		return False

# --------------------------------------------------------------------

def serve_file(user, uid, slug, fileid, serve_type):
	response = None
	if allowed_in_project(user, uid, slug) or core_u.is_admin(user):
		document = get_object_or_404(repo_m.Document, pk=fileid)
		with document.docfile as f:
			wrapper = FileWrapper(f)
			response = HttpResponse(wrapper, content_type=document.mime_type)
			response['Content-Length'] = f.size
			if serve_type == "download":
				response['Content-Disposition'] = 'attachment; filename="%s"' \
				% document.filename()
			else:
				response['Content-Disposition'] = 'inline; filename="%s"' \
				% document.filename()
	else:
		return HttpResponseForbidden()

	return response

# --------------------------------------------------------------------

def file_is_uploaded_by(file, user):
	if file.uploaded_by == user:
		return True
	else:
		return False

# --------------------------------------------------------------------

def delete_file(user, uid, slug, fileid):
	is_admin = core_u.is_admin(user)
	if allowed_in_project(user, uid, slug) or is_admin:
		try:
		    file  = repo_m.Document.objects.get(pk=fileid)
		except ObjectDoesNotExist:
		    file = None

		if file is not None:
			if file_is_uploaded_by(file, user) or is_admin:
				project = repo_m.Project.objects.get(uid=uid, slug=slug)

				add_project_log(project, "Deleted a file: %s" % file.filename(), user)

				file.delete()
				return "existent"
			else:
				return "forbidden"
				
		else:
			return "inexistent"
	else:
		return "forbidden"

# --------------------------------------------------------------------

def get_journal_events(project_owner, start = None, end = None):
	journal_events = repo_m.Event.objects.filter(
		project_owner__uid=project_owner,
		event_type = "journal"
	)

	if start != "" and end != "":
		start_object = datetime.datetime.strptime(start,'%B %d, %Y')
		end_object = datetime.datetime.strptime(end,'%B %d, %Y')
		journal_events = journal_events.filter(
				start_date__gte=start_object,
				end_date__lte=end_object
			)

	elif start != "":
		start_object = datetime.datetime.strptime(start,'%B %d, %Y')
		journal_events = journal_events.filter(
				start_date__gte=start_object
			)

	elif end != "":
		end_object = datetime.datetime.strptime(end,'%B %d, %Y')
		journal_events = journal_events.filter(
				end_date__lte=end_object
			)

	return journal_events.order_by('start_date')

# --------------------------------------------------------------------

def get_used_storage_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)

    size_bytes = Byte(total_size)
    size_mb = size_bytes.to_MB()
    return round(size_mb, 2)

# --------------------------------------------------------------------

def get_working_files_capacity():
	cap = Setting.objects.get(name="working_files_capacity").value
	cap = float(cap)

	return cap

# --------------------------------------------------------------------

def get_percentage(size):
	cap = get_working_files_capacity()
	result = 100 * (size/cap)
	return round(result, 2)

# --------------------------------------------------------------------

def check_if_sufficient(path, files):
	used_storage = get_used_storage_size(path)

	to_upload_total_size = 0
	for file in files:
		to_upload_total_size += file.size

	size_bytes = Byte(to_upload_total_size)

	total = used_storage + size_bytes.to_MB()

	if total <= 20:
		return True
	else:
		return False

# --------------------------------------------------------------------

def save_file(file, owner, uploaded_by, official):
	newdoc = repo_m.Document(docfile = file)
	newdoc.owner = owner
	newdoc.mime_type = file.content_type
	newdoc.uploaded_by = uploaded_by

	if official:
		newdoc.official = True

	newdoc.save()

	add_project_log(owner, "Uploaded a file: %s" % newdoc.filename(), uploaded_by)

	return newdoc

# --------------------------------------------------------------------

def change_status(project, status):
	project.update(status=status)

# --------------------------------------------------------------------

def start_publication(user, uid, slug):
	if core_u.is_coor(user, uid, slug):
		if project_is_ongoing(uid, slug):
			project = repo_m.Project.objects.filter(uid=uid, slug=slug)
			change_status(project, "publication")
		else:
			print "HINDI ONGOING"
	else:
		print "HINDI COORDINATOR"

# --------------------------------------------------------------------

def start_confirmation(user, uid, slug):
	if core_u.is_student(user):
		if user_is_member(user, uid, slug):
			project = repo_m.Project.objects.filter(uid=uid, slug=slug)
			if project[0].status == "publication":
				pre_final = repo_m.Document.objects.filter(
						owner__uid=uid,
						official = True
					)

				if pre_final:
					change_status(project, "confirmation")
				else:
					print "Official list is empty"
			else:
				print "Project is not ready for confirmation"
		else:
			print "Only a member could start the confimation"
	else:
		print "Only students could start the confirmation"

# --------------------------------------------------------------------

def start_processing(user, uid, slug):
	if core_u.is_coor(user, uid, slug):
		project = repo_m.Project.objects.filter(uid=uid, slug=slug)
		change_status(project, "processing")
		tasks.start_processing.delay(uid, slug)
	else:
		print "Not coordinator"

# --------------------------------------------------------------------

def get_search(form, project_status, user):
	to_search = form.cleaned_data['search']
	keywords = to_search.split()

	status = None
	result = None

	if project_status == "published":
		result = repo_m.Project.objects.filter(
			reduce(operator.or_, (
					Q(title__icontains=x, status="published") for x in keywords
				)
			)
		)
	else:
		if core_u.is_admin(user):
			projects = repo_m.Project.objects.exclude(
				status="published")

			result = projects.filter(
				reduce(operator.or_, (
						Q(title__icontains=x) for x in keywords
					)
				)
			)

		else:
			ongoing_projects = get_ongoing_projects(user)
			result = ongoing_projects.filter(
				reduce(operator.or_, (
						(Q(title__icontains=x) & ~Q(status="published"))for x in keywords
					)
				)
			)

	return result

# --------------------------------------------------------------------

def get_available_advisers(assignments):
	courses = []
	for assignment in assignments:
		courses.append(assignment.course)

	advisers = None
	if len(courses) != 0:
		advisers = Course_Faculty_Assignment.objects.filter(
			reduce(operator.or_, (
					Q(assignment="adviser", course = x) for x in courses
				)
			)
		)

	return advisers

# --------------------------------------------------------------------

def leave_group(project, membership, user):
	if bool(membership):
		to_delete = repo_m.Project_Membership.objects.get(
			pk=membership)
		message = None
		actor = None
		to_return = None

		if project.status != "published":
			if to_delete.project == project:
				if to_delete.member == user:
					message = "Left the group: %s %s" % (user.first_name, user.last_name)
					to_delete.delete()
				elif core_u.is_coor(user) or core_u.is_admin(user):
					message = "removed %s %s in the project" % (
						to_delete.member.first_name, 
						to_delete.member.last_name)
					actor = user
					to_delete.delete()

					to_return = True
				else:
					return HttpResponseForbidden()
			else:
				return HttpResponseForbidden()
		else:
			return HttpResponseForbidden()

	log = repo_m.Project_Log()

	if actor:
		log.actor = actor

	log.project_log = project
	log.message = message
	log.save()

	return to_return

# --------------------------------------------------------------------

def get_advisoree_requests(user, assignment_adviser):
	requests = repo_m.Project_Adviser_Request.objects.filter(
		reduce(operator.or_, (
				Q(requested = x, accepted=None) for x in assignment_adviser
			)
		)
	)

	return requests

# --------------------------------------------------------------------

def allowed_in_project(user, uid, slug):
	
	is_admin = core_u.is_admin(user)
	is_coor = core_u.is_coor(user, uid, slug)
	is_adviser = core_u.is_adviser(user, uid, slug)
	is_member = user_is_member(user, uid, slug)

	if is_coor or is_adviser or is_member or is_admin:
		return True
	else:
		return False

# --------------------------------------------------------------------

def get_notifications(projects, user):
	try:
	    last_visit = repo_m.User_Last_Visit_Ongoing.objects.get(
	    	user=user
	    )

	    last_visit = last_visit.last_visit
	except ObjectDoesNotExist:
	    return None


	notifications = repo_m.Project_Log.objects.filter(
		reduce(operator.or_, (
				Q(project_log = x, created_date__gte=last_visit) for x in projects
			)
		)
	)

	return notifications

# --------------------------------------------------------------------

def get_near_events(projects):
	one_day = timezone.now().date() + datetime.timedelta(days=1)
	two_day = timezone.now().date() + datetime.timedelta(days=2)

	events = repo_m.Event.objects.filter(
		reduce(operator.or_, (
				(Q(project_owner = x) & Q(start_date=one_day) | Q(start_date=two_day)) for x in projects
			)
		)
	)

	if events.count() != 0:
		events = events.filter(project_owner__status="ongoing")
	else:
		events = None

	return events

# --------------------------------------------------------------------

def add_project_log(project, message, user = None):
	sem = get_current_sem()
	ssy = get_current_ssy()
	esy = get_current_esy()

	log = repo_m.Project_Log()
	log.actor = user
	log.project_log = project
	log.message = message
	log.semester = sem
	log.start_sy = ssy
	log.end_sy = esy
	log.save()

# --------------------------------------------------------------------

def has_ongoing(user):
	if core_u.is_student(user):
		if repo_m.Project.objects.filter(members=user,status="ongoing").exists():
			return True
		else:
			return False
	else:
		return False

# --------------------------------------------------------------------

def get_current_sem():
	return Setting.objects.get(name="semester").value

# --------------------------------------------------------------------

def get_current_ssy():
	return Setting.objects.get(name="start_school_year").value

# --------------------------------------------------------------------

def get_current_esy():
	return Setting.objects.get(name="end_school_year").value
