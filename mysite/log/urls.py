# log/urls.py

from django.urls import path

from . import views

urlpatterns = [
    # 127.0.0.1:8000/log/
    path('', views.index, name='index'),
]