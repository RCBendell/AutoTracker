from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
   # return HttpResponse("Hello, World. You're at the log index.")
   context = {}
   return render(request, 'index.html', context = context)
