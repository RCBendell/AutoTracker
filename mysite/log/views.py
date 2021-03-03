from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# For SignUpView
from log.forms import SignUpForm, CarCreationForm, LogEntryForm

from django.contrib.auth.models import User

from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import car, entry
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
class profile(ListView):
   model = entry
   template_name = 'profile.html'

   def get_queryset(self):
      return entry.objects.filter(owner = self.request.user.get_username()).order_by('-date_time')

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

   def get_context_data(self, *args, **kwargs):
      context = super(carDetail, self).get_context_data(*args, **kwargs)
      number = self.request.path
      # Path is /car/<int:pk>... Returning after 5 characters, enables only the <int:pk> to show up
      number = number[5:]
      context['entry_list'] = entry.objects.filter(car = number)
      return context

class carUpdate(UpdateView):
   model = car
   template_name = 'car_update.html'
   fields = ['make','model', 'year', 'color', 'mileage', 'vin', 'image']

class carDelete(DeleteView):
   model = car
   template_name = 'car_delete.html'
   success_url = reverse_lazy('myGarage')

# Create Log Entry
def createEntry(request):
   if request.method == 'POST':
      form = LogEntryForm(request.user, request.POST)
      if form.is_valid():
         obj = form.save(commit=False)
         obj.owner = request.user.get_username()
         form.save()
         return redirect('profile')
   else:
      form = LogEntryForm(request.user)
   return render(request, 'entry_creation.html', {'form': form})

class entryList(ListView):
   model = car
   template_name = 'entry_list.html'

class entryUpdate(UpdateView):
   model = entry
   template_name = 'entry_update.html'
   fields = ['car', 'blog', 'cost']
   sucess_url = reverse_lazy('profile')

class entryDetail(DetailView):
   model = entry
   template_name = 'entry_detail.html'
