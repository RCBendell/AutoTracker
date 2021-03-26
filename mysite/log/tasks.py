from celery import shared_task, app
from django.utils.timezone import now
from .models import reminder, car

from django.template.loader import render_to_string
from django.core.mail import send_mail
#from django.contrib.auth.models import User
import datetime
from django.contrib.sites.shortcuts import get_current_site

@shared_task()
def say_hello():
    print('Hello')

@shared_task()
def add(x, y):
    return x+y

@shared_task()
def send_reminder_email(r):
    # Only works when hosting Locally
    domain = '127.0.0.1:8000/' 
    subject = 'AutoTracker Reminder!'
    message = render_to_string('reminder_email.html', 
    {
        'txt': r.msg,
        'date': r.remind_on_date,
        'carInstance': r.car,
        'identification': r.id,
        'domain': domain,
        # 'new_date': r.remind_on_date + 1 day
    })
    send_mail(subject, 
                message, 
                'bendell.test01@gmail.com', 
                [r.email],
                fail_silently = False, 
    )

    print('Email Sent!')

# I need a task that runs on startup, perhaps called from profile view

# Then it needs to repeat, every 24 hours

# I might need to change all date fields to datetime fields in order to test this 

# First make it a normal task and create a reminder that expired already

# This needs to find reminder, compare to current date, send email if date it past

# then it needs to delete reminder from database

@shared_task()
def check_reminders():
    reminder_list = reminder.objects.all()
    
    if reminder_list:
        for x in reminder_list:
            y = x.remind_on_date
            z = datetime.date.today()
            if y <= z:
                print('This One')
                send_reminder_email(x)
    
@shared_task()
def update_mileage(obj):
    if obj.car.mileage < obj.update_mileage:
        obj.car.mileage = obj.update_mileage
    obj.car.save()
    