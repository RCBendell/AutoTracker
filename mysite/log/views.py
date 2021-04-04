from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# For SignUpView
from log.forms import SignUpForm, CarCreationForm, LogEntryForm, reminderForm

from django.contrib.auth.models import User

from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import car, entry, reminder
from django.urls import reverse_lazy

from log.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .tokens import account_activation_token

from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text, force_bytes

from .tasks import say_hello, add, send_reminder_email, check_reminders, update_mileage
import datetime

from django.db.models import Sum, Min, Max
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator


# Index View
def index(request):
   context = {}
   #check_reminders.delay()
   #say_hello.delay()
   check_reminders.apply_async(countdown=10)
   return render(request, 'index.html', context = context)




from django.views.generic import View
from rest_framework.views import APIView 
from rest_framework.response import Response 

from django.http import JsonResponse

# Returns cost data for the last year of an individual vehicle
# Used on Car Detail Chart
def expenditurepercar_chart(request, pk):

   qs = entry.objects.filter(owner=request.user.get_username())
   qs = qs.filter(car = pk)
   
   today = datetime.date.today()
   start = datetime.date.today()
   start = start.replace(year=datetime.date.today().year-1)
   if datetime.date.today().day >= 30:
      start = start.replace(day=datetime.date.today().day-5)
   start = start.replace(month=datetime.date.today().month+1)

   qs = qs.filter(date__range=[start, today])
   beginMonth = start.month
   # begin at start.month and increment 12 times
   labels = []
   cost_data = [] 
   mileage_data = [] 

   for i in range (1,13):
      labels.append(beginMonth)
      if beginMonth <12:
         beginMonth +=1
      else: 
         beginMonth = 1

   for i in range (1,13):
      cost_data.append(0.00)
      mileage_data.append(0)

   for x in qs:
      y = labels.index(x.date.month)
      value = cost_data[y]+float(x.cost)
      cost_data.pop(y)
      cost_data.insert(y, value)

   # Labels are still by month
   # need to calculate changes in mileage
   # have qs
   # need to break down entries by month, find the latest one with highest mileage,
   # Subtract that from the Previous Months
   min_mileage = qs.aggregate(Min('update_mileage')).get('update_mileage__min', 0)

   # Go by month
   for i in range (1,13):
      # i is the index 
      y = labels[i-1]
      # now y is the month 
      # New QuerySet by month
      qs_month = qs.filter(date__month = y)

      if min_mileage == 0:
         min_mileage = qs_month.aggregate(Min('update_mileage')).get('update_mileage__min', 0)

      if qs_month:
         max_mileage = qs_month.aggregate(Max('update_mileage')).get('update_mileage__max', 0)
         #min_mileage = qs_month.aggregate(Min('update_mileage')).get('update_mileage__min', 0)
      else:
         max_mileage = 0
         min_mileage = 0

      if max_mileage == None or min_mileage == None:
         max_mileage = 0
         min_mileage = 0
      
      difference = max_mileage - min_mileage
      
      mileage_data.pop(i-1)
      mileage_data.insert(i-1, difference)

      min_mileage = max_mileage
      max_mileage = min_mileage + 1


   labels.clear()
   beginMonth = start.month
   for i in range(1,13):
      datetime_object = datetime.datetime.strptime(str(beginMonth), "%m")
      month_name = datetime_object.strftime("%B")

      labels.append(month_name)
      if beginMonth <12:
         beginMonth +=1
      else: 
         beginMonth = 1

   return JsonResponse(data={
      'labels': labels, 
      'data': cost_data,
      'mdata': mileage_data,
   })

# Returns cost data of the last yeat for an individual user
# Used on Profile page chart
def expenditure_chart(request):

   qs = entry.objects.filter(owner=request.user.get_username())
   
   today = datetime.date.today()
   start = datetime.date.today()
   start = start.replace(year=datetime.date.today().year-1)
   if datetime.date.today().day >= 30:
      start = start.replace(day=datetime.date.today().day-5)
   start = start.replace(month=datetime.date.today().month+1)

   qs = qs.filter(date__range=[start, today])
   beginMonth = start.month
   # begin at start.month and increment 12 times
   labels = []
   data = []  

   for i in range (1,13):
      labels.append(beginMonth)
      if beginMonth <12:
         beginMonth +=1
      else: 
         beginMonth = 1

   for i in range (1,13):
      data.append(0.00)

   for x in qs:
      y = labels.index(x.date.month)
      value = data[y]+float(x.cost)
      data.pop(y)
      data.insert(y, value)

   labels.clear()
   beginMonth = start.month
   for i in range(1,13):
      datetime_object = datetime.datetime.strptime(str(beginMonth), "%m")
      month_name = datetime_object.strftime("%B")

      labels.append(month_name)
      if beginMonth <12:
         beginMonth +=1
      else: 
         beginMonth = 1

   return JsonResponse(data={
      'labels': labels, 
      'data': data,
   })


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

   def get_context_data(self, *args, **kwargs):
      context = super(profile, self).get_context_data(*args, **kwargs)
      context['reminder_list'] = reminder.objects.filter(owner = self.request.user.get_username())#.order_by('-date')
      return context

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
      #send_reminder_email()
      return car.objects.filter(owner = self.request.user.get_username())

class carDetail(DetailView):
   model = car
   template_name = 'car_detail.html'

   def get_context_data(self, *args, **kwargs):
      context = super(carDetail, self).get_context_data(*args, **kwargs)
      number = self.request.path
      # Path is /car/<int:pk>... Returning after 5 characters, enables only the <int:pk> to show up
      number = number[5:]
      context['entry_list'] = entry.objects.filter(car = number).order_by('-date')
      context['total'] = entry.objects.filter(car=number).aggregate(Sum('cost')).get('cost__sum', 0.00)
      return context

class carUpdate(UpdateView):
   model = car
   template_name = 'car_update.html'
   fields = ['make','model', 'year', 'color', 'vin', 'image', 'is_inspected', 'inspected_exp', 'is_registered', 'registered_exp', 'is_insured', 'insured_exp']

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

         update_mileage(obj)

         form.save()
         return redirect('profile')
   else:
      form = LogEntryForm(request.user)
   return render(request, 'entry_creation.html', {'form': form})



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

# Create Reminder
def createReminder(request):
   if request.method == 'POST':
      form = reminderForm(request.user, request.POST)
      if form.is_valid():
         oby = form.save(commit=False)
         oby.owner = request.user.get_username()
         oby.email = request.user.email

         form.save()
         return redirect('profile')
   else:
      form = reminderForm(request.user)
   return render(request, 'reminder_creation.html', {'form': form})

class reminderDetail(DetailView):
   model = reminder
   template_name = 'reminder_detail.html'

class reminderUpdate(UpdateView):
   model = reminder
   template_name = 'reminder_update.html'
   fields = ['msg', 'remind_on_date']

class reminderDelete(DeleteView):
   model = reminder
   template_name = 'reminder_delete.html'
   success_url = reverse_lazy('profile')

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "registration/password_reset_email.html"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset_form.html", context={"password_reset_form":password_reset_form})


def diagnosticData(request):
   context = {}
   context['user_count'] = User.objects.count()
   context['entry_count'] = entry.objects.count()
   context['car_count'] = car.objects.count()
   context['reminder_count'] = reminder.objects.count()
   return render(request, 'diagnostic_data.html', context = context)

def new_users_chart(request):
   qs = User.objects.all()
   
   today = datetime.date.today()
   start = datetime.date.today()
   start = start.replace(year=datetime.date.today().year-1)
   if datetime.date.today().day >= 30:
      start = start.replace(day=datetime.date.today().day-5)
   start = start.replace(month=datetime.date.today().month+1)

   qs = qs.filter(date_joined__range=[start, today])
   
   beginMonth = start.month
   # begin at start.month and increment 12 times
   labels = []
   data = []  

   for i in range (1,13):
      labels.append(beginMonth)
      if beginMonth <12:
         beginMonth +=1
      else: 
         beginMonth = 1

   for i in range (1,13):
      data.append(0)

   for x in qs:
      y = labels.index(x.date_joined.month)
      value = data[y]+1
      data.pop(y)
      data.insert(y, value)

   labels.clear()
   beginMonth = start.month
   for i in range(1,13):
      datetime_object = datetime.datetime.strptime(str(beginMonth), "%m")
      month_name = datetime_object.strftime("%B")

      labels.append(month_name)
      if beginMonth <12:
         beginMonth +=1
      else: 
         beginMonth = 1

   return JsonResponse(data={
      'labels': labels, 
      'data': data,
   })

def new_entries_chart(request):
   qs = entry.objects.all()
   
   today = datetime.date.today()
   start = datetime.date.today()
   start = start.replace(year=datetime.date.today().year-1)
   if datetime.date.today().day >= 30:
      start = start.replace(day=datetime.date.today().day-5)
   start = start.replace(month=datetime.date.today().month+1)

   qs = qs.filter(date__range=[start, today])
   
   beginMonth = start.month
   # begin at start.month and increment 12 times
   labels = []
   data = []  

   for i in range (1,13):
      labels.append(beginMonth)
      if beginMonth <12:
         beginMonth +=1
      else: 
         beginMonth = 1

   for i in range (1,13):
      data.append(0)

   for x in qs:
      y = labels.index(x.date.month)
      value = data[y]+1
      data.pop(y)
      data.insert(y, value)

   labels.clear()
   beginMonth = start.month
   for i in range(1,13):
      datetime_object = datetime.datetime.strptime(str(beginMonth), "%m")
      month_name = datetime_object.strftime("%B")

      labels.append(month_name)
      if beginMonth <12:
         beginMonth +=1
      else: 
         beginMonth = 1

   return JsonResponse(data={
      'labels': labels, 
      'data': data,
   })

#ADMIN List Views
class entryList(ListView):
   model = entry
   template_name = 'entry_list.html'

class carList(ListView):
   model = car
   template_name = 'car_list.html'

class reminderList(ListView):
   model = reminder
   template_name = 'reminder_list.html'

class userList(ListView):
   model = User
   template_name = 'user_list.html'