from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from admin_control.models import Course, Course_Faculty_Assignment
import os
import uuid
from django.conf import settings
from django.dispatch import receiver

from PyPDF2 import PdfFileReader
from wand.image import Image

# --------------------------------------------------------------------

class Project(models.Model):
	# Attributes
    title          = models.CharField(max_length=200, unique=True)
    abstract       = models.TextField(max_length=200, blank=True, null=True)
    created_date   = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    secret_code    = models.CharField(max_length=50)
    slug           = models.TextField()
    uid            = models.UUIDField(default=uuid.uuid4, editable=False)
    status         = models.CharField(max_length=200, default="ongoing")

	# Relations
    members     = models.ManyToManyField(User, through='Project_Membership')
    coordinator = models.ForeignKey(
        Course_Faculty_Assignment, related_name="coordinator"
    )
    adviser = models.ForeignKey(
		Course_Faculty_Assignment, related_name="adviser",
		blank = True, null = True
	)

	# Methods
    def __unicode__(self):
        return self.title

# --------------------------------------------------------------------

class Project_Membership(models.Model):
	# Attributes
    added_date = models.DateTimeField(default=timezone.now)

	# Relations
    project = models.ForeignKey(Project, related_name='project')
    member  = models.ForeignKey(User, related_name='member')


	# Methods
    def __unicode__(self):
        return self.project.title

# --------------------------------------------------------------------

class Event(models.Model):
	# Attributes
    title      = models.CharField(max_length=50)
    start_date = models.DateField(null=True)
    end_date   = models.DateField(null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time   = models.TimeField(blank=True, null=True)
    event_type = models.CharField(max_length=50, null=True)
    notes      = models.TextField(null=True, blank=True)

	# Relations
    project_owner    = models.ForeignKey(Project, related_name='project_owner', blank=True, null=True)
    course_owner = models.ForeignKey(Course_Faculty_Assignment, related_name='course_owner', blank=True, null=True)
    posted_by        = models.ForeignKey(User, related_name='posted_by')
    included_members = models.ManyToManyField(User, through='Event_Actor')

	# Methods
    def __unicode__(self):
        return self.title

# --------------------------------------------------------------------

class Event_Actor(models.Model):
    # Relations
    event = models.ForeignKey(Event, related_name="event")
    member = models.ForeignKey(User, related_name="included_member")

    # Methods
    def __unicode__(self):
        return self.event.title

# --------------------------------------------------------------------

def generate_filename(self, filename):
    url = "docpriv/%s/%s" % (self.owner.id, filename)
    return url

# --------------------------------------------------------------------

class Document(models.Model):
	# Attributes
    docfile      = models.FileField(upload_to=generate_filename)
    mime_type    = models.CharField(max_length=255)
    official     = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    # Relations
    owner       = models.ForeignKey(Project, related_name='owner')
    uploaded_by = models.ForeignKey(User, related_name='uploaded_by')

    # Methods
    def filename(self):
        return os.path.basename(self.docfile.name)

    def __convert_to_img__(self, width, height, format='jpg'):
    	size = ''
        if width and height:
            size = '_' + str(width) + 'x' + str(height) + 'px'

        # FILE PATH
        filename = self.docfile.name
        filepath = settings.MEDIA_ROOT + '/' + filename
        
        output_dir = "%s/public/image_docs/%s/" % (settings.MEDIA_ROOT, self.owner.uid)

        os.mkdir(output_dir)

        input_file = PdfFileReader(file(filepath, 'rb'))

        for i in range(input_file.getNumPages()):
            with Image(filename = filepath + '[' + str(i) + ']', 
                resolution=100) as img:
                if len(size) > 0:
                    img.resize(width, height)

                img.format = format
                img.save(filename = output_dir + str(i) + '.' + format)

    def convert_to_png(self, width=0, height=0):
        self.__convert_to_img__(width, height, 'png')

    def convert_to_jpg(self, width=0, height=0):
        self.__convert_to_img__(width, height, 'jpg')

# --------------------------------------------------------------------

@receiver(models.signals.post_delete, sender=Document)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `Document` object is deleted.
    """
    if instance.docfile:
        if os.path.isfile(instance.docfile.path):
            os.remove(instance.docfile.path)

# --------------------------------------------------------------------

class Project_Log(models.Model):
    # Attributes
    message      = models.TextField(max_length=255)
    created_date = models.DateTimeField(default=timezone.now)
    semester   = models.CharField(max_length=50)
    start_sy   = models.CharField(max_length=50)
    end_sy     = models.CharField(max_length=50)

    # Relations
    project_log = models.ForeignKey(Project, related_name='project_log', null=True, blank=True)
    course_log = models.ForeignKey(Course_Faculty_Assignment, related_name='course_log', null = True, blank = True)
    actor   = models.ForeignKey(User, related_name='actor', null=True)

    # Methods
    def __unicode__(self):
        return self.message

# --------------------------------------------------------------------

class Project_Adviser_Request(models.Model):
    # Relations
    requester = models.ForeignKey(Project, related_name='requester')
    requested = models.ForeignKey(
        Course_Faculty_Assignment, related_name="requested",
    )
    accepted = models.NullBooleanField(null=True)

    def __unicode__(self):
        return self.requester.title

# --------------------------------------------------------------------

class User_Last_Visit_Ongoing(models.Model):
    # Attributes
    last_visit = models.DateTimeField(null=True)

    # Relations
    user = models.ForeignKey(User, related_name="user")

    def __unicode__(self):
        return str(self.last_visit)

# --------------------------------------------------------------------

class User_Docu_Request(models.Model):
    user = models.ForeignKey(User, related_name="docu_requester")
    req_docs = models.ForeignKey(Project, related_name='req_docs')
    semester   = models.CharField(max_length=50)
    start_sy   = models.CharField(max_length=50)
    end_sy     = models.CharField(max_length=50)
    access = models.NullBooleanField(null=False)

    def __unicode__(self):
        return str(self.user.username)

admin.site.register(Project)
admin.site.register(User_Docu_Request)
admin.site.register(Project_Membership)
admin.site.register(Event)
admin.site.register(Document)
admin.site.register(Project_Adviser_Request)
