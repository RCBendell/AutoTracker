from django.db import models

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
