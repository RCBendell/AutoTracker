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

from log.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .tokens import account_activation_token

from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text, force_bytes

# Index View
def index(request):
   context = {}
   return render(request, 'index.html', context = context)

# View for using sign up form
def signup(request):
   if request.method == 'POST':
      form = SignUpForm(request.POST)
      if form.is_valid():
         ser = form.save(commit = False)
         ser.is_active = False

         ser.save()

         current_site = get_current_site(request)
         subject = 'Activate your AutoTracker Account'
         message = render_to_string('account_activation_email.html',
         {
            'user': ser, 
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(ser.pk)),
            'token': account_activation_token.make_token(ser),
         })

         send_mail(subject, 
                     message, 
                     'bendell.test01@gmail.com', 
                     [ser.email], 
                     
                     fail_silently = False, 
         )

         return redirect('account_activation_sent')

   else:
      form = SignUpForm()
   return render(request, 'signup.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


#def activate(request, uidb64, token):
#   uid = force_text(urlsafe_base64_decode(uidb64))
#   user = User.objects.get(pk=uid)
#   user.is_active = True
#   user.save()
#   login(request, user)
#   return redirect('index')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('index')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# Profile View
class profile(ListView):
   model = entry
   template_name = 'profile.html'

   def get_queryset(self):
      return entry.objects.filter(owner = self.request.user.get_username()).order_by('-date')

# Create A New Car
def createCar(request):
   if request.method == 'POST':
      form = CarCreationForm(request.POST, request.FILES)
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
   fields = ['make','model', 'year', 'color', 'mileage', 'vin', 'image', 'is_inspected', 'inspected_exp', 'is_registered', 'registered_exp', 'is_insured', 'insured_exp']

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
   fields = ['car', 'blog', 'cost', 'date']
   sucess_url = reverse_lazy('profile')

class entryDetail(DetailView):
   model = entry
   template_name = 'entry_detail.html'

# Used in Profile View
def searchResults(request):
   sch = request.GET['query']
   # Searches search keyword
   entry_list = entry.objects.filter(blog__icontains=sch)
   # Makes sure owner is correct, orders
   entry_list = entry_list.filter(owner = request.user.get_username()).order_by('-date')
   context = {'entry_list':entry_list, 'search':sch}

   return render(request, 'search_results.html', context)

#def carSearchResults(request):
 #  sch = request.GET['query']
   # Searches search keyword
  # entry_list = entry.objects.filter(blog__icontains=sch)
   # Makes sure owner is correct, orders
   #entry_list = entry_list.filter(owner = request.user.get_username()).order_by('-date')

   #number = request.path
   # Path is /carsearch/<int:pk>... Returning after 5 characters, enables only the <int:pk> to show up
   #number = number[11:]
   #entry_list = entry_list.filter(car = number)

   #context = {'entry_list':entry_list, 'search':sch}

   #return render(request, 'search_results.html', context)