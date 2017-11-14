from django.conf.urls import include, url
from . import views


urlpatterns = [
	url(r'^$', views.manage),
	url(r'^courses/$', views.courses),	
	url(r'^programs/$', views.programs),	
	url(r'^add_course/$', views.add_course),	
	url(r'^add_program/$', views.add_program),	
	url(r'^edit_course/$', views.edit_course),	
	url(r'^edit_program/$', views.edit_program),	

	url(r'^assignments/$', views.assignments),	
	url(r'^add_assignment/$', views.add_assignment),

	url(r'^settings/$', views.settings),	
	url(r'^save_settings/$', views.save_settings),

	url(r'^users/$', views.users),	
	url(r'^add_user/$', views.add_user),	
]
