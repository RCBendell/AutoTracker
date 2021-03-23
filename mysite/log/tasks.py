from celery import shared_task, app
from django.utils.timezone import now

@shared_task()
def say_hello():
    print('Hello')

@shared_task()
def add(x, y):
    return x+y
