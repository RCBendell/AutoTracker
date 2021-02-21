# log/urls.py

from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    # 127.0.0.1:8000/log/
    path('', views.index, name='index'),
    # Signup/Account Creation
    url(r'^signup/$', views.signup, name='signup'),
    # Profile View?
    url(r'^profile/$', views.profile, name='profile'),
    # Add Car
    url(r'^createCar/$', views.createCar, name='createCar'),
]