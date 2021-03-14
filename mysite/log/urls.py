# log/urls.py

from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # 127.0.0.1:8000/log/
    path('', views.index, name='index'),
    # Signup/Account Creation
    url(r'^signup/$', views.signup, name='signup'),
    # Profile View -- OLD
    #url(r'^profile/$', views.profile, name='profile'),
    # Profile View with Entry List
    path('profile/', views.profile.as_view(), name='profile'),
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
    url(r'^createEntry/$', views.createEntry, name='createEntry'),
    # Edit Entry
    path('entry/<int:pk>/update/', views.entryUpdate.as_view(), name='entryUpdate'),
    # Entry Detail View
    path('entry/<int:pk>', views.entryDetail.as_view(), name='entryDetail'),

    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    #url(r'^activate/(?P<uidb64>.+)/(?P<token>.+)/$', views.activate, name='activate'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', views.activate, name='activate'),

    path('search/', views.searchResults, name='searchResults'),

    #path('carsearch/<int:pk>', views.carSearchResults, name='carSearchResults'),
    
]
if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 