from django import forms
from django.contrib.auth.models import User, Group
from repository.models import Project_Membership, Project
from django.core.exceptions import ValidationError
from repository.models import Project, Project_Log

# --------------------------------------------------------------------

class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(
        widget = forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'First Name',
                }
            ),
        required=True
    )

    last_name = forms.CharField(
        widget = forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Last Name',
                }
            ),
        required=True
    )

    username = forms.CharField(
        widget = forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Username',
                }
            ),
        required=True
    )

    email = forms.CharField(
        widget = forms.EmailInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Email',
                }
            ),
        required=True
    )

    password = forms.CharField(
        widget = forms.PasswordInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Password',
                }
            ),
    )

    confirm_password = forms.CharField(
        widget = forms.PasswordInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Confirm Password',
                }
            ),
        required=True
    )

    project_secret_code = forms.CharField(
        widget = forms.PasswordInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Project Secret Code',
                }
            ),
        required=True
    )

    def save_membership(self):
        user = self.save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()

        group = Group.objects.get(name="students")
        group.user_set.add(user)

        project = Project.objects.get(
                secret_code = self.cleaned_data[
                        'project_secret_code'
                    ]
            )

        membership = Project_Membership()
        membership.project = project
        membership.member = user
        membership.save()

        log = Project_Log()
        log.project_log = project
        log.message = "Joined the project: %s %s" % (user.first_name, user.last_name)
        log.save()

        return user

    def clean_password(self):
        password = self.cleaned_data['password']

        # Minimum 8
        if len(password) < 8:
            raise ValidationError("Minimum password length is 8")

        # Maximum 14
        if len(password) > 14:
            raise ValidationError("Maximum password length is 14")

        return password


    def clean_confirm_password(self):
        if "password" not in self.cleaned_data:
            raise ValidationError("Please provide a valid password")

        confpass = self.cleaned_data['confirm_password']
        password = self.cleaned_data['password']

        if confpass != password:
            raise ValidationError("Password does not match.")

    def clean_project_secret_code(self):
        secret_code = self.cleaned_data['project_secret_code']

        project = Project.objects.filter(secret_code=secret_code)

        if project:
            if project.get().status == "published":
                raise ValidationError("Project code is expired!")
        else:
            raise ValidationError("Project code does not exist.")

        return secret_code


    class Meta:
        model = User
        fields = ('first_name','last_name','username','email',
                  'password')

# --------------------------------------------------------------------

class AccountManagementForm(forms.ModelForm):

    first_name = forms.CharField(
        widget = forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'First Name',
                }
            ),
        required=True
    )

    last_name = forms.CharField(
        widget = forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Last Name',
                }
            ),
        required=True
    )

    username = forms.CharField(
        widget = forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Username',
                }
            ),
        required=True
    )

    email = forms.CharField(
        widget = forms.EmailInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Email',
                }
            ),
        required=True
    )

    class Meta:
        model = User
        fields = ('first_name','last_name','email','username')

# --------------------------------------------------------------------

class NewPassForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(NewPassForm, self).__init__(*args, **kwargs)


    current_password = forms.CharField(
        widget = forms.PasswordInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Current Password',
                }
            ),
    )

    password = forms.CharField(
        widget = forms.PasswordInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'New Password',
                }
            ),
    )

    confirm_password = forms.CharField(
        widget = forms.PasswordInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Confirm Password',
                }
            ),
        required=True
    )

    def clean_current_password(self):
        password = self.cleaned_data['current_password']
        if not self.user.check_password(password):
            raise ValidationError('Invalid password')

    def clean_confirm_password(self):
        confpass = self.cleaned_data['password']
        password = self.cleaned_data['confirm_password']

        if confpass != password:
            raise ValidationError("Password does not match.")

    def update_password(self):
        password = self.cleaned_data['password']
        self.user.set_password(password)
        self.user.save()

    class Meta:
        model = User
        fields = ('current_password','password','confirm_password')
