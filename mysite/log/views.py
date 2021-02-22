from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# For SignUpView
from log.forms import SignUpForm, CarCreationForm

from django.contrib.auth.models import User

from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import car
from django.urls import reverse_lazy

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
   return render(request, 'profile.html')

# Create A New Car
def createCar(request):
   if request.method == 'POST':
      form = CarCreationForm(request.POST)
      if form.is_valid():
         obj = form.save(commit=False)
         obj.owner = request.user.get_username()
         form.save()
         return redirect('profile')
   else:
      form = CarCreationForm()
   return render(request, 'car_creation.html', {'form': form})

class myGarage(ListView):
   model = car
   template_name = 'my_garage.html'
   
   def get_queryset(self):
      return car.objects.filter(owner = self.request.user.get_username())

class carDetail(DetailView):
   model = car
   template_name = 'car_detail.html'

class carUpdate(UpdateView):
   model = car
   template_name = 'car_update.html'
   fields = ['make','model', 'year', 'color', 'mileage', 'vin']

class carDelete(DeleteView):
   model = car
   template_name = 'car_delete.html'
   success_url = reverse_lazy('myGarage')


