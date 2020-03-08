from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from accounts.forms import AlumniSignUpForm, FacultySignUpForm, AccountAuthenticationForm
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
        return redirect('base:home')

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
        return redirect('base:home')

def signup_view(request):
    return render(request, 'account/signup.html')


#
# def signup_view(request):
#     context = {}
#     if request.POST:
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             raw_password = form.cleaned_data.get('password1')
#             account = authenticate(email=email, password=raw_password)
#             login(request, account)
#             return redirect('base:home')
#         else:
#             context['registration_form'] = form
#     else:
#         form = RegistrationForm()
#         context['registration_form'] = form
#     return render(request, 'account/signup.html', context)

def logout_view(request):
    logout(request)
    return redirect("base:home")


def login_view(request):

    context = {}

    user=request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            user=authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("base:home")

    else:
        form=AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)
