from django import forms
from .models import Project, Project_Membership, Event, Document, Project_Log, Event_Actor
from admin_control.models import Course, Course_Faculty_Assignment, Setting
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.text import slugify
import datetime
import pytz
from multiupload.fields import MultiFileField
from django_select2 import forms as ds2



from .utils import (
    create_secret_code, add_project_log
)

# --------------------------------------------------------------------

class AddProjectForm(forms.ModelForm):
    def save_project(self):
        coordinator = self.cleaned_data['coordinator']
        project_title = self.cleaned_data['title']
        project = self.save(commit=False)
        project.slug = slugify(project_title)
        project.coordinator = coordinator
        project.save()

        secret_code = create_secret_code()
        current_project = Project.objects.filter(pk=project.id)
        current_project.update(secret_code=secret_code)

        return project.id

    class Meta:
        model = Project
        fields = ('title','coordinator')
        widgets = {
            'title': forms.TextInput(
            	attrs = {
	            	'class': 'form-control',
	            	'placeholder': 'Project Title',
        		},
        	),
        }

# --------------------------------------------------------------------

class EditTitleForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'New Project Title',
                },
            ),
        }

# --------------------------------------------------------------------

class AddMemberForm(forms.ModelForm):
    def save_members(self, user, current_project_obj, actor):
        membership = self.save(commit=False)
        membership.project = current_project_obj
        membership.member = User.objects.get(pk=user)
        membership.save()

        to_add = User.objects.get(pk=user)

        add_project_log(
            current_project_obj,
            "added a member: %s %s" % (to_add.first_name, to_add.last_name),
            actor
        )

        return to_add

    user = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='Students'),
        widget = ds2.ModelSelect2MultipleWidget(
                attrs = {
                    'class': 'form-control',
                    'style': 'width: 100%'
                },
                search_fields = ['username__icontains',]
            )
        )

    class Meta:
        model = Project_Membership
        fields = ('user',)

# --------------------------------------------------------------------

class AddProgressEventForm(forms.ModelForm):
    def update(self, members, event):
        title = self.cleaned_data['title']
        progress_event = self.save(commit=False)
        progress_event.notes = self.cleaned_data['notes']

        start_date = self.cleaned_data['start_date']
        start = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        end = start + datetime.timedelta(days=1)
        progress_event.end_date = end

        progress_event.save()

        event.included_members.clear()

        for member in members:
            temp = Event_Actor()
            temp.event = progress_event
            temp.member = User.objects.get(pk=member)
            temp.save()


    def save_event(self, posted_by, owner, event_type, members):
        title = self.cleaned_data['title']
        progress_event = self.save(commit=False)
        progress_event.posted_by = posted_by
        progress_event.project_owner = owner
        progress_event.event_type = event_type
        progress_event.notes = self.cleaned_data['notes']

        start_date = self.cleaned_data['start_date']
        start = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        end = start + datetime.timedelta(days=1)
        progress_event.end_date = end

        add_project_log(
            owner,
            "added a journal event on the calendar: %s" % title,
            posted_by
        )

        progress_event.save()

        for member in members:
            temp = Event_Actor()
            temp.event = progress_event
            temp.member = User.objects.get(pk=member)
            temp.save()

    title = forms.CharField(
            widget = forms.TextInput(
                attrs = {
                    'class' : 'form-control'
                }
            )
        )

    start_date = forms.CharField(
            widget = forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                }
            )
        )

    end_date = forms.CharField(
            widget = forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                }
            )
        )

    notes = forms.CharField(
            widget = forms.Textarea(
                attrs = {
                    'class' : 'form-control',
                    'rows' : '3',
                }
            )
        )

    class Meta:
        model = Event
        fields = ('title','start_date','end_date')

# --------------------------------------------------------------------

class AddDeadlineEvent(forms.ModelForm):
    def update(self):
        deadline_event = self.save(commit=False)
        start_date = self.cleaned_data['start_date']
        start = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        end = start + datetime.timedelta(days=1)
        deadline_event.end_date = end
        deadline_event.notes = self.cleaned_data['notes']
        

        start_time = self.cleaned_data['start_time']
        if start_time != "Invalid date":
            deadline_event.start_time = start_time

        deadline_event.save()


    def save_event(self, posted_by, owner, event_type, course = None):
        title = self.cleaned_data['title']
        deadline_event = self.save(commit=False)
        deadline_event.posted_by = posted_by
        deadline_event.project_owner = owner
        deadline_event.event_type = event_type
        deadline_event.notes = self.cleaned_data['notes']

        start_date = self.cleaned_data['start_date']
        start = datetime.datetime.strptime(start_date,'%Y-%m-%d')
        end = start + datetime.timedelta(days=1)
        deadline_event.end_date = end

        if course == None:
            deadline_event.project_owner = owner
        else:
            deadline_event.course_owner = course


        start_time = self.cleaned_data['start_time']
        if start_time != "Invalid date":
            deadline_event.start_time = start_time

        add_project_log(
            owner,
            "added a deadline event on the calendar: %s" % title,
            posted_by
        )

        deadline_event.save()

    title = forms.CharField(
            widget = forms.TextInput(
                attrs = {
                    'class' : 'form-control'
                }
            )
        )

    start_date = forms.CharField(
            widget = forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                }
            )
        )

    start_time = forms.CharField(
            widget = forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                }
            )
        )

    notes = forms.CharField(
            widget = forms.Textarea(
                attrs = {
                    'class' : 'form-control',
                    'rows' : '3',
                }
            )
        )

    class Meta:
        model = Event
        fields = ('title','start_date')

# --------------------------------------------------------------------

class DocumentForm(forms.Form):
    docfile = MultiFileField(min_num=1)

    class Meta:
        model = Document
        fields = ('docfile', )

# --------------------------------------------------------------------

class OfficialDocumentForm(forms.Form):
    docfile = MultiFileField(min_num=1, max_num=1)

    def clean_docfile(self):
        file = self.cleaned_data['docfile']
        for each in file:
            if each.content_type != "application/pdf":
                raise forms.ValidationError("PDF file only.")

    class Meta:
        model = Document
        fields = ('docfile', )

# --------------------------------------------------------------------

class TermCourseForm(forms.ModelForm):
    def save_assignment(self, course, adviser):
        response = {}
        admin_settings = Setting.objects.all()

        current_start_sy = admin_settings.get(name="start_school_year").value
        current_end_sy = admin_settings.get(name="end_school_year").value
        current_sem = admin_settings.get(name="semester").value

        course_instance = Course.objects.get(id=course) 
        adviser_instance = User.objects.get(id=adviser)

        if Course_Faculty_Assignment.objects.filter(
                assignment = "adviser",
                faculty = adviser_instance,
                course = course_instance,
                start_sy = current_start_sy,
                end_sy = current_end_sy,
                semester = current_sem
            ).exists():
            response['errors'] = "%s %s can already be an adviser of \
            %s this %s semester, SY %s - %s" % (
                    adviser_instance.first_name,
                    adviser_instance.last_name,
                    course_instance.name,
                    current_sem,
                    current_start_sy,
                    current_end_sy
                )
            response['valid'] = False
        else:
            assignment = self.save(commit=False)
            assignment.start_sy = current_start_sy
            assignment.end_sy = current_end_sy
            assignment.semester = current_sem
            assignment.assignment = "adviser"
            assignment.course = course_instance
            assignment.faculty = adviser_instance
            assignment.accepted = False
            assignment.save()
            
            response['valid'] = True
            response['course'] = course_instance.name
            response['coordinator'] = "%s %s" % (
                  adviser_instance.first_name,
                  adviser_instance.last_name
              )

        return response

    faculty = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='faculty'),
        widget = ds2.Select2Widget(
            attrs = {
                    'class' : 'form-control',
                    'style' : 'width: 100%'
                }
            )
        )

    class Meta:
        model = Course_Faculty_Assignment
        fields = ('faculty','course')

# --------------------------------------------------------------------

class SearchForm(forms.Form):
    search = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
                'type' : 'text',
                'placeholder' : 'Search keywords in project title'
                }
            )
        )

# --------------------------------------------------------------------

class AbstractForm(forms.Form):
    def update_abstract(self, project, user):
        new_abstract = self.cleaned_data['abstract']
        project.update(abstract=new_abstract)

        add_project_log(
            project.get(),
            "edited the abstract",
            user
        )

        return new_abstract

    abstract = forms.CharField(
            widget = forms.Textarea(
                attrs = {
                    'class' : 'form-control',
                    'rows' : '20',
                }
            )
        )

    class Meta:
        model = Project
        fields = ('abstract',)

# --------------------------------------------------------------------

