"""
Django settings for thesismates project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

from __future__ import absolute_import
# ^^^ The above is required if you want to import from the celery
# library.  If you don't have this then `from celery.schedules import`
# becomes `proj.celery.schedules` in Python 2.x since it allows
# for relative imports by default.

# Celery settings

BROKER_URL = 'amqp://guest:guest@localhost:5672//'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Sessions
SESSION_SECURITY_WARN_AFTER = 60*4
SESSION_SECURITY_EXPIRE_AFTER = 60*5
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*axmjr8w@fo@g2a2cn2r4%ma71%5om73na3$(mg8gci&(bdkxj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'admin_control',
    'django_ajax',
    'community',
    'repository',
    'easy_pdf',
    'djcelery',
    'dbbackup',
    'django_select2',
    'pretty_times',
    'watermarker',
    'session_security',
    'widget_tweaks'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
)

ROOT_URLCONF = 'thesismates.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'thesismates.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'thesismates',
        'USER': 'root',
        'PASSWORD': 'kamote0310',
        'HOST': '127.0.0.1',
        # 'PORT': '5432',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

TMP_DIR = os.path.join(BASE_DIR, 'temp')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(os.path.dirname(__file__),'static'),
)

STATIC_URL = '/static/'

LOGIN_URL = '/'

# Back up settings DROPBOX

DBBACKUP_STORAGE = 'dbbackup.storage.dropbox_storage'
DBBACKUP_TOKENS_FILEPATH = 'lFOMZZoD1TAAAAAAAAAAI26bi8Oq-dyo1HDNBNL1ATP-d-CAJPRcJdQVYcFdjBiI'
DBBACKUP_DROPBOX_APP_KEY = '6usriq41cea2fc4'
DBBACKUP_DROPBOX_APP_SECRET = 'q1ioyykncby7408'

AUTHENTICATION_BACKENDS = ['django-dual-authentication.backends.DualAuthentication']


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'shinjimaru01@gmail.com'
EMAIL_HOST_PASSWORD = 'ewanko1029031020'
DEFAULT_FROM_EMAIL = 'shinjimaru01@gmail.com'



