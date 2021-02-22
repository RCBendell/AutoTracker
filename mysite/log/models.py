from django.db import models
from django.urls import reverse

# Create your models here.
class car(models.Model):
    owner = models.CharField(max_length=20)
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.PositiveSmallIntegerField()
    # Optional
    color = models.CharField(max_length=15, blank=True)
    # Optional
    vin = models.CharField(max_length=30, blank=True, unique=True)
    mileage = models.PositiveIntegerField()
    # Optional 
    # image = models.ImageField(blank=True)
    # Need to Install Something ... 

    def get_absolute_url(self):
        return reverse('carDetail', args=[str(self.id)])
