from __future__ import absolute_import
from django.core.mail import send_mail
from celery import shared_task

@shared_task
def send_invitation(message_body, email):
	title = 'Welcome to Thesismates!'
	mail_from = 'shinjimaru01@gmail.com'
	message = message_body

	send_mail(title, message, mail_from, [email,], fail_silently=False)

