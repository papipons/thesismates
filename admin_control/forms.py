from django import forms
from .models import Course, Setting, Course_Faculty_Assignment, Program
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_select2 import forms as ds2

# --------------------------------------------------------------------

class CourseForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(CourseForm, self).clean()
        name = cleaned_data['name']
        program = cleaned_data['program']

        if Course.objects.filter(name=name, program=program).exists():
            raise forms.ValidationError({'name':"Course with the selected program already exists"})

        return cleaned_data

    class Meta:
        model = Course
        fields = ('name', 'program')
        widgets = {
            'name': forms.TextInput(
            	attrs = {
	            	'class': 'form-control',
	            	'placeholder': 'Course Name',
        		},
        	),
            'program' : ds2.Select2Widget(
                attrs = {
                    'class' : 'form-control'
                }
            )
        }

# --------------------------------------------------------------------

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ('code', 'name', 'description')
        widgets = {
            'code': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Program Code',
                },
            ),
            'name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Program Name',
                },
            ),
            'description': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Description',
                },
            ),
        }


# --------------------------------------------------------------------

class SemForm(forms.ModelForm):
    class Meta:
        sem_choices = (
            ('1st' , '1st'),
            ('2nd' , '2nd'),
            ('summer', 'summer')
        )

        model = Setting
        fields = ('value',)
        widgets = {
            'value': ds2.Select2Widget(
                attrs = {
                    'class' : 'form-control'
                },
                choices = sem_choices,
            )

        }

# --------------------------------------------------------------------

class CapacityForm(forms.ModelForm):
    class Meta:
        cap_choices = (
            ('20' , '20'),
            ('30' , '30'),
            ('40' , '40'),
            ('50' , '50')
        )

        model = Setting
        fields = ('value',)
        widgets = {
           'value': ds2.Select2Widget(
               attrs = {
                   'class' : 'form-control'
               },
               choices = cap_choices,
           )

        }

# --------------------------------------------------------------------

class SyForm(forms.ModelForm):
    class Meta:
        year_choices = (
            ('2015-2016' , '2015 - 2016'),
            ('2016-2017' , '2016 - 2017'),
            ('2017-2018' , '2017 - 2018'),
            ('2018-2019' , '2018 - 2019'),
            ('2019-2020' , '2019 - 2020'),
            ('2020-2021' , '2020 - 2021')
        )

        model = Setting
        fields = ('value',)
        widgets = {
            'value': ds2.Select2Widget(
                attrs = {
                    'class' : 'form-control'
                },
                choices = year_choices,
            )
        }

# --------------------------------------------------------------------

class TermCourseForm(forms.ModelForm):
    def save_assignment(self, course, coordinator):
        admin_settings = Setting.objects.all()

        current_start_sy = admin_settings.get(name="start_school_year").value
        current_end_sy = admin_settings.get(name="end_school_year").value
        current_sem = admin_settings.get(name="semester").value

        course_instance = Course.objects.get(id=course) 
        coordinator_instance = User.objects.get(id=coordinator)

        response = {}

        if Course_Faculty_Assignment.objects.filter(
                course = course_instance,
                start_sy = current_start_sy,
                end_sy = current_end_sy,
                semester = current_sem,
                assignment = "coordinator"
            ).exists():
            response['errors'] = "%s already has a coordinator \
            this %s semester, SY %s - %s" % (
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
            assignment.assignment = "coordinator"
            assignment.save()
            
            response['valid'] = True
            response['course'] = course_instance.name
            response['coordinator'] = "%s %s" % (
                  coordinator_instance.first_name,
                  coordinator_instance.last_name
              )
            response['assignment'] = "Coordinator"
            response['semester'] = current_sem
            response['start_school_year'] = current_start_sy
            response['end_school_year'] = current_end_sy

        return response

    faculty = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='faculty'),
        widget = ds2.Select2Widget(
            attrs = {
                    'class' : 'form-control',
                }
            )
        )

    class Meta:
        model = Course_Faculty_Assignment
        fields = ('course', 'faculty')
        widgets = {
            'course': ds2.Select2Widget(
                attrs = {
                    'class' : 'form-control'
                }
            )
        }

# --------------------------------------------------------------------

class AdminAddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : 'Email'
                },
            ),
        }
