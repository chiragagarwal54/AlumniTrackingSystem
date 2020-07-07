from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import Alumni, Faculty, User
from base.models import Event, Notice, News
from jobs.models import Job

def base(request):
    return render(request, 'base.html')

def home(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        if user.is_alumni:
            alumni = Alumni.objects.get(user=user)
            if not user.profile_complete:
                return redirect('accounts:complete_alumni_profile')
            context['is_alumni']=1
            context['is_faculty']=0
            context['alumni']=alumni
        elif user.is_faculty:
            faculty = Faculty.objects.get(user=user)
            if not user.profile_complete:
                return redirect('accounts:complete_faculty_profile')
            context['is_alumni']=0
            context['is_faculty']=1
            context['faculty']=faculty
        else:
            context['is_superuser']=1
    events = Event.objects.all().order_by('-date_time')
    if(events.count()<3):
        context['eventsitem']=events
    else:
        context['eventsitem']=events[0:3]
    news = News.objects.all().order_by('-date_time')
    if(news.count()<3):
        context['newsitem']=news
    else:
        context['newsitem']=news[0:3]
    jobs = Job.objects.all().order_by('-date_created')
    if(jobs.count()<2):
        context['jobsitem']=jobs
    else:
        context['jobsitem']=jobs[0:2]

    return render(request, 'home.html', context)
