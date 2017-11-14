"""thesismates URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from repository import views

urlpatterns = [
    url(r'', include('core.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^select2/', include('django_select2.urls')),
    url(r'session_security/', include('session_security.urls')),
    url(r'^user/password/reset/$', 
            'django.contrib.auth.views.password_reset', 
            {'post_reset_redirect' : '/user/password/reset/done/'},
            name="password_reset"),
    url(r'^user/password/reset/done/$',
            'django.contrib.auth.views.password_reset_done'),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
            'django.contrib.auth.views.password_reset_confirm', 
            {'post_reset_redirect' : '/user/password/done/'},
            name="password_reset_confirm"),
    url(r'^user/password/done/$', 
            'django.contrib.auth.views.password_reset_complete')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
