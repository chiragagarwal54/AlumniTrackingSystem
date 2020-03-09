from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.http import HttpResponse
from accounts.forms import AlumniSignUpForm, FacultySignUpForm, AccountAuthenticationForm, CompleteAlumniProfile, CompleteFacultyProfile
from django.views.generic import CreateView, ListView, UpdateView
from accounts.models import User

class alumni_signup_view(CreateView):
    model = User
    form_class = AlumniSignUpForm
    template_name = 'account/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Alumni'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts:complete_alumni_profile')

class faculty_signup_view(CreateView):
    model = User
    form_class = FacultySignUpForm
    template_name = 'account/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Faculty'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts:complete_faculty_profile')

def signup_view(request):
    return render(request, 'account/signup.html')

def complete_alumni_profile(request):

    context = {}

    user=request.user

    if request.POST:
        form=CompleteAlumniProfile(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('base:home')

    else:
        form = CompleteAlumniProfile(request.user)

    context['profile_form']=form
    return render(request, 'account/complete_alumni_profile.html', context)

def complete_faculty_profile(request):

    context = {}

    user=request.user

    if request.POST:
        form=CompleteFacultyProfile(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('base:home')

    else:
        form = CompleteFacultyProfile(request.user)

    context['profile_form']=form
    return render(request, 'account/complete_faculty_profile.html', context)


def logout_view(request):
    logout(request)
    return redirect("base:home")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('base:home')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'account/login.html')

# def login_view(request):
#
#     user=request.user
#     if user.is_authenticated:
#         return redirect("base:home")
#
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#     else


    # context = {}
    #
    # user=request.user
    # if user.is_authenticated:
    #     return redirect("base:home")
    #
    # if request.POST:
    #     form = AccountAuthenticationForm(request.POST)
    #     if form.is_valid():
    #         email=request.POST['email']
    #         password=request.POST['password']
    #         user=authenticate(request, email=email, password=password)
    #
    #         if user:
    #             login(request, user)
    #             return redirect("base:home")
    #
    # else:
    #     form=AccountAuthenticationForm()
    #
    # context['login_form'] = form
    # return render(request, 'account/login.html', context)
