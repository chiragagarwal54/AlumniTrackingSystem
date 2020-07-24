from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import Alumni, Faculty, User
from base.models import Event, Notice, News, Story
from jobs.models import Job
from django.db.models import Q
import datetime
from django.http import JsonResponse


def base(request):
    return render(request, "base.html")


def home(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        if user.is_alumni:
            alumni = Alumni.objects.get(user=user)
            if not user.profile_complete:
                return redirect("accounts:complete_alumni_profile")
            context["is_alumni"] = 1
            context["is_faculty"] = 0
            context["alumni"] = alumni
        elif user.is_faculty:
            faculty = Faculty.objects.get(user=user)
            if not user.profile_complete:
                return redirect("accounts:complete_faculty_profile")
            context["is_alumni"] = 0
            context["is_faculty"] = 1
            context["faculty"] = faculty
        else:
            context["is_superuser"] = 1
    events = Event.objects.all().order_by("-start_date")
    if events.count() < 3:
        context["eventsitem"] = events
    else:
        context["eventsitem"] = events[0:3]
    news = News.objects.all().order_by("-date_time")
    if news.count() < 3:
        context["newsitem"] = news
    else:
        context["newsitem"] = news[0:3]
    jobs = Job.objects.all().order_by("-date_created")
    if jobs.count() < 2:
        context["jobsitem"] = jobs
    else:
        context["jobsitem"] = jobs[0:2]

    story = Story.objects.all().order_by("-date_time")
    if story.count() > 0:
        context["storyitem"] = story[0]

    return render(request, "home.html", context)


def allnews(request):
    context = {}
    news = News.objects.all()
    context["news"] = news

    return render(request, "all-news.html", context)


def allevents(request):
    context = {}
    today = datetime.datetime.today()
    upcoming_events = Event.objects.filter(Q(start_date__gte=today))
    past_events = Event.objects.filter(Q(start_date__lte=today))
    context["upcoming_events"] = upcoming_events
    context["past_events"] = past_events

    return render(request, "all-events.html", context)


def speceficevent(request, event_id):
    context = {}
    event = Event.objects.get(id=event_id)
    context["event"] = event

    return render(request, "specific-event.html", context)


def speceficnews(request, news_id):
    context = {}
    news = News.objects.get(id=news_id)
    context["news"] = news

    return render(request, "specefic-news.html", context)


def speceficstory(request, story_id):
    context = {}
    story = Story.objects.get(id=story_id)
    context["story"] = story

    return render(request, "specefic-story.html", context)


def profile(request, user_name, user_id):
    context = {}
    user = User.objects.get(id=user_id)
    if user.is_alumni:
        alumni = Alumni.objects.get(user=user)
        context["is_alumni"] = 1
        context["is_faculty"] = 0
        context["alumni"] = alumni
    elif user.is_faculty:
        faculty = Faculty.objects.get(user=user)
        context["is_alumni"] = 0
        context["is_faculty"] = 1
        context["faculty"] = faculty
    context["user"] = user
    context["editprofile"] = 0
    if user == request.user:
        context["editprofile"] = 1

    return render(request, "profile.html", context)


def searchalumni(request):
    context = {}
    query = ""

    if request.GET:
        query = request.GET["q"]

    context = get_queryset(str(query))
    context["query"] = str(query)

    return render(request, "search_alumni.html", context)


def get_queryset(query=None):
    queryset = {}
    if query:
        alumnis = (
            User.objects.filter(Q(full_name__icontains=query))
            .filter(is_alumni=1)
            .distinct()
        )
        queryset["users"] = alumnis
    return queryset


def autocomplete(request):
    if "term" in request.GET:
        qs = (
            User.objects.filter(Q(full_name__icontains=request.GET["term"]))
            .filter(is_alumni=True)
            .distinct()
        )
        names = list()
        for name in qs:
            names.append(name.full_name)
        return JsonResponse(names, safe=False)
    return JsonResponse({}, safe=False)

def jobsection(request):
    context = {}
    jobs=Job.objects.all()
    context['jobsitem']=jobs
    return render(request,'all-jobs.html',context)
