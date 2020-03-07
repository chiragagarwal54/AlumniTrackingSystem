from django.shortcuts import render, redirect
from django.urls import reverse

def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')
