from django.db import models
from django.urls import reverse
import datetime
import uuid
from datetime import date

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
    image = models.ImageField(blank=True, upload_to='media/uploaded_images/')
    
    is_inspected = models.BooleanField(null=True)
    inspected_exp = models.DateField(blank=True, null=True)

    is_registered = models.BooleanField(null=True)
    registered_exp = models.DateField(blank=True, null=True)

    is_insured = models.BooleanField(null=True)
    insured_exp = models.DateField(blank=True, null=True)

    # DateField.auto_now_add() = True

    def get_absolute_url(self):
        return reverse('carDetail', args=[str(self.id)])

    def __str__(self):
        return '%s %s %s' % (self.year, self.make, self.model)

class entry(models.Model):
    car = models.ForeignKey(car, on_delete=models.CASCADE)
    owner = models.CharField(max_length=20, blank=False)
    modified_date_time = models.DateTimeField(auto_now=True)
    date = models.DateField(default=date.today)
    blog = models.TextField()
    #update_mileage = models.PositiveIntegerField()
    
    # Optional ... It might not have cost anything, might just be saying hey
    cost = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)
    # File for receipts
    
    # If you have a warranty, make it true, else it will be assumed there is no warranty for the entry
    # warranty = models.BooleanField(default=False)
    # Images

    def get_absolute_url(self):
        return reverse('entryDetail', args=[str(self.id)])

class reminder(models.Model):
    # type, date, or mileage triggered. 
    # Build date first
    remind_on_date = models.DateField(blank=False)
    # Whos is it, for searching purposes
    owner = models.CharField(max_length=20, blank=False)
    # Recipient(owner's email)
    email = models.EmailField(blank=False)
    # Car id for which car it belongs too
    car = models.ForeignKey(car, on_delete=models.CASCADE)
    # What the reminder is about
    msg = models.TextField()

    def get_absolute_url(self):
        return reverse('reminderDetail', args=[str(self.id)])


