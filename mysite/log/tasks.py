from celery import shared_task
from django.utils.timezone import now

@shared_task()
def say_hello():
    print('Hello')
