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
    # My Garage
    path('myGarage/', views.myGarage.as_view(), name='myGarage'),
    # Car Detail Page .. Needs to have list of recent log entries, recent first
    path('car/<int:pk>', views.carDetail.as_view(), name='carDetail'),
    # Edit Car Details .. Everything Editable except Owner
    path('car/<int:pk>/update/', views.carUpdate.as_view(), name='carUpdate'),
    # Delete Car  .. OR a method for deleting a car in a garage
    path('car/<int:pk>/delete/', views.carDelete.as_view(), name='carDelete'),
    # New Entry .. Add a Log Entry Associated with the Car

]