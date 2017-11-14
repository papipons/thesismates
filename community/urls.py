from django.conf.urls import include, url
from . import views


urlpatterns = [
	url(r'^$', views.community),
	url(r'^ask_question/$', views.ask_question),	
	url(r'^accept/(?P<response>[-\w\d]+)/(?P<id>[-\w\d]+)$', views.accept),	
	url(r'^reject/(?P<response>[-\w\d]+)/(?P<id>[-\w\d]+)$', views.reject),	
	url(r'^search/$', views.get_search),	
	url(r'^(?P<id>[-\w\d]+)/(?P<slug>[-\w\d]+)/$', views.question),
	url(r'^(?P<id>[-\w\d]+)/(?P<slug>[-\w\d]+)/answer/$', views.answer),
]
