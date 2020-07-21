from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import Alumni, Faculty, User
from base.models import Event, Notice, News, Story
from jobs.models import Job
from django.db.models import Q
import datetime

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
    events = Event.objects.all().order_by('-start_date')
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

    story=Story.objects.all().order_by('-date_time')
    if(story.count()>0):
        context['storyitem']=story[0]

    return render(request, 'home.html', context)

def allnews(request):
    context = {}
    news=News.objects.all()
    context['news']=news

    return render(request, 'all-news.html', context)

def allevents(request):
    context = {}
    today = datetime.datetime.today()
    upcoming_events = Event.objects.filter(Q(start_date__gte=today))
    past_events = Event.objects.filter(Q(start_date__lte=today))
    context['upcoming_events']=upcoming_events
    context['past_events']=past_events

    return render(request, 'all-events.html', context)

def speceficevent(request, event_id):
    context = {}
    event = Event.objects.get(id=event_id)
    context['event']=event

    return render(request, 'specific-event.html', context)

def speceficnews(request, news_id):
    context = {}
    news = News.objects.get(id=news_id)
    context['news']=news

    return render(request, 'specefic-news.html', context)

def profile(request, user_name, user_id):
    context = {}
    user = User.objects.get(id=user_id)
    if(user.is_alumni):
        alumni = Alumni.objects.get(user=user)
        context['is_alumni']=1
        context['is_faculty']=0
        context['alumni']=alumni
    elif(user.is_faculty):
        faculty = Faculty.objects.get(user=user)
        context['is_alumni']=0
        context['is_faculty']=1
        context['faculty']=faculty
    context['user'] = user
    context['editprofile']=0
    if(user==request.user):
        context['editprofile']=1

    return render(request,'profile.html', context)

def searchalumni(request):
    context = {}
    query = ""

    if request.GET:
        query = request.GET['q']

    context = get_queryset(str(query))
    context['query'] = str(query)

    return render(request, 'search_alumni.html', context)

def get_queryset(query=None):
    queryset = {}
    queries = query.split(" ")
    if query:
        for q in queries:
            alumnis = User.objects.filter(
                    Q(first_name__icontains=q) or Q(last_name__icontains=q)).filter(is_alumni=1).distinct()

            queryset['users'] = alumnis

    return queryset
