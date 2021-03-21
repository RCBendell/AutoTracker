"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
# from django.conf.urls import url
# from mysite.core import views as core_views
from django.conf import settings
from django.conf.urls.static import static
from log import views



urlpatterns = [
    # 127.0.0.1:8000/log
    path('', include('log.urls')),
    # 127.0.0.1:8000/admin
    path('admin/', admin.site.urls),
    # Adds account handling
    path('accounts/', include('django.contrib.auth.urls')),
    # Signup/Account Creation
    # url(r'^signup/$', core_views.signup, name='signup'),
    # I think this goes in the other one

    # For rendering a chart 
    path('expenditurepercar-chart/<int:pk>/', views.expenditurepercar_chart, name='expenditurepercar-chart'),
    path('expenditure-chart/', views.expenditure_chart, name='expenditure-chart'),
] 

if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 
