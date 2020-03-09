from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import Alumni, Faculty, User

def base(request):
    return render(request, 'base.html')

def home(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        if user.is_alumni:
            alumni = Alumni.objects.get(user=user)
            if not alumni.profile_complete:
                return redirect('accounts:complete_alumni_profile')
            context['is_alumni']=1
            context['is_faculty']=0
            context['alumni']=alumni
        elif user.is_faculty:
            faculty = Faculty.objects.get(user=user)
            if not faculty.profile_complete:
                return redirect('accounts:complete_faculty_profile')
            context['is_alumni']=0
            context['is_faculty']=1
            context['faculty']=faculty
        else:
            context['is_superuser']=1
    return render(request, 'home.html', context)
