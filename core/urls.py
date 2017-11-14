from django.conf.urls import include, url
from . import views


urlpatterns = [
	url(r'^$', views.index),
	url(r'^logout/$', views.log_out),
	url(r'^signup/$', views.sign_up),
	url(r'^account/$', views.account),
	url(r'^manage/', include('admin_control.urls')),
	url(r'^projects/', include('repository.urls')),
	url(r'^community/', include('community.urls')),
]
