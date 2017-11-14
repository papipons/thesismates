from django.conf.urls import include, url
from . import views



urlpatterns = [
	# Get projects : project_status = "ongoing", "unpublished"
	url(r'^(?P<project_status>[-\w\d]+)/$', views.projects),
	url(r'^(?P<project_status>[-\w\d]+)/search/$', views.get_search),

	# Project Profile
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/$', views.project_profile),
	url(r'^(?P<project_status>[-\w\d]+)/generate_report/$', views.generate_report),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/profile$', views.profile),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/calendar$', views.calendar),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/files$', views.files),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/log$', views.log),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/get_user_for_delete$', views.get_user_for_delete),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/leave_group$', views.leave_group),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/request_adviser/$', views.request_adviser),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/(?P<response>[-\w\d]+)/respond_advisoree_request/$', views.respond_advisoree_request),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/documentation$', views.view_documentation),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/start_publication$', views.start_publication),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/start_confirmation/$', views.start_confirmation),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/start_processing/$', views.start_processing),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/rejection/$', views.rejection),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/edit_abstract/$', views.edit_abstract),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/edit_title/$', views.edit_title),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/doc_req/$', views.doc_req),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/get_event_instance/$', views.get_event_instance),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/save_manual/$', views.save_manual),

	# Specific Project controls
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/files$', views.files),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/add_member/$', views.add_member),

	# Calendar 
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/get_events/$', views.get_events),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/add_event/$', views.add_event),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/save_event_changes/$', views.save_event_changes),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/remove_event/$', views.remove_event),

	# Files
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/upload_file/$', views.upload_file),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/delete_file/(?P<fileid>[-\w\d]+)$', views.delete_file),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/download/(?P<fileid>[-\w\d]+)$', views.download_file),
	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/view/(?P<fileid>[-\w\d]+)$', views.view_file),

	url(r'^(?P<project_status>[-\w\d]+)/(?P<uid>[-\w\d]+)/(?P<slug>[-\w\d]+)/journal$', views.generate_journal),

	# Global Project controls
	url(r'^(?P<project_status>[-\w\d]+)/add_project/$', views.add_project),
	url(r'^(?P<project_status>[-\w\d]+)/add_event/$', views.add_event),
	url(r'^(?P<project_status>[-\w\d]+)/assign_advisers/$', views.assign_advisers),
] 
