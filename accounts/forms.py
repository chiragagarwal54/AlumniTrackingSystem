from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.db import transaction
from college.models import College, Department
from accounts.models import Alumni, Faculty, User

class AlumniSignUpForm(UserCreationForm):
    college = forms.ModelChoiceField(
        queryset=College.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_alumni = True
        user.save()
        alumni = Alumni.objects.create(user=user)
        alumni.college = College.objects.get(college)
        return user


class FacultySignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_faculty = True
        if commit:
            user.save()
        return user


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
