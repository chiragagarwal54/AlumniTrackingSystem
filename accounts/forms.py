from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.db import transaction
import datetime
from college.models import College, Department
from accounts.models import Alumni, Faculty, User

def year_choices():
    return [(r,r) for r in range(1947, datetime.date.today().year+1)]

class AlumniSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    college = forms.ModelChoiceField(queryset=College.objects.all(), required=True)
    unique_id = forms.CharField(max_length=200)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_alumni = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.college = College.objects.get(name=self.cleaned_data['college'])
        user.save()
        unique_id = self.cleaned_data['unique_id']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email_address = self.cleaned_data['email']
        system_date_joined = datetime.datetime.now()

        alumni = Alumni.objects.create(
            user=user,
            unique_id=unique_id,
            )
        return user

class FacultySignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    college = forms.ModelChoiceField(queryset=College.objects.all(), required=True)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_faculty = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email_address = self.cleaned_data['email']
        user.college = College.objects.get(name=self.cleaned_data['college'])
        user.save()
        system_date_joined = datetime.datetime.now()

        faculty = Faculty.objects.create(
            user=user,
            )
        return user

class CompleteAlumniProfile(forms.ModelForm):

    department_choices = Department.objects.all()

    department = forms.ModelChoiceField(queryset=department_choices, required=True)
    dob = forms.DateField()
    year_of_passing = forms.ChoiceField(choices=year_choices())

    class Meta:
        model = Alumni
        fields = ('dob', 'department', 'year_of_passing')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CompleteAlumniProfile, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = self.user
        alumni = Alumni.objects.get(user=self.user)
        user.department = Department.objects.get(name=self.cleaned_data['department'])
        user.dob = self.cleaned_data['dob']
        alumni.year_of_passing = self.cleaned_data['year_of_passing']
        user.profile_complete=1
        alumni.save()
        user.save()

class CompleteFacultyProfile(forms.ModelForm):

    department_choices = Department.objects.all()

    department = forms.ModelChoiceField(queryset=department_choices, required=True)
    dob = forms.DateField()
    college_joined_year = forms.ChoiceField(choices=year_choices())
    research_interest = forms.CharField(max_length=300)

    class Meta:
        model = Alumni
        fields = ('dob', 'department', 'college_joined_year', 'research_interest')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CompleteFacultyProfile, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = self.user
        faculty = Faculty.objects.get(user=self.user)
        user.department = Department.objects.get(name=self.cleaned_data['department'])
        user.dob = self.cleaned_data['dob']
        faculty.college_joined_year = self.cleaned_data['college_joined_year']
        faculty.research_interest = self.cleaned_data['research_interest']
        user.profile_complete=1
        faculty.save()
        user.save()

class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            password=self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")

class UpdateAlumniProfile(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'college', 'department', 'dob')
