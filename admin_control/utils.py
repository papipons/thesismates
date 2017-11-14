from django.contrib.auth.models import User, Group
from . import tasks
from django.template.loader import render_to_string


# --------------------------------------------------------------------

def create_username(email,rand_string):
	import random

	username = ''
	for x in email:
		if x == "@":
			break
		else:
			username += x

	shuffled_rand_string = ''.join(
			random.sample(rand_string,len(rand_string))
		)

	username += shuffled_rand_string

	return username

# --------------------------------------------------------------------

def create_user_send_invite(email):
	response = {}
	rand_string = User.objects.make_random_password(length=8)
	# rand_string = "password"

	if email:
		user, created = User.objects.get_or_create(email=email)

		if created:
			user.set_password(rand_string)
			user.username = create_username(email,rand_string)
			user.save()
			
			group = Group.objects.get(name="faculty")
			group.user_set.add(user)

			context = {
				'password' : rand_string,
			}
			
			message = render_to_string('admin_control/email_template.html', context)

			tasks.send_invitation.delay(message, email)
			response['valid'] = True

		else:
			response['valid'] = False
			response['errors'] = "%s is already in use" % email

	else:
		response['valid'] = False
		response['errors'] = "Please fill up the email field."

	return response
