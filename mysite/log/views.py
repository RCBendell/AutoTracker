from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# For SignUpView
from log.forms import SignUpForm, CarCreationForm

from django.contrib.auth.models import User

# Index View
def index(request):
   context = {}
   return render(request, 'index.html', context = context)

# View for using sign up form
def signup(request):
   if request.method == 'POST':
      form = SignUpForm(request.POST)
      if form.is_valid():
         form.save()
         username = form.cleaned_data.get('username')
         raw_password = form.cleaned_data.get('password1')
         user = authenticate(username=username, password=raw_password)
         login(request, user)
         return redirect('index')
   else:
      form = SignUpForm()
   return render(request, 'signup.html', {'form': form})

# Profile View
def profile(request):
   #context = {}
   return render(request, 'profile.html')
  # return HttpResponse("Hello, You've Made it")

# Create A New Car
def createCar(request):
   if request.method == 'POST':
      form = CarCreationForm(request.POST)
      if form.is_valid():
         #owner = self.username
         form.save()
         return redirect('profile')
   else:
      form = CarCreationForm()
   return render(request, 'car_creation.html', {'form': form})