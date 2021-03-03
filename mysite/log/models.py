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
    image = models.ImageField(blank=True, upload_to='uploaded_images/')
    

    # DateField.auto_now_add() = True

    def get_absolute_url(self):
        return reverse('carDetail', args=[str(self.id)])

    def __str__(self):
        return '%s %s %s' % (self.year, self.make, self.model)

class entry(models.Model):
    car = models.ForeignKey(car, on_delete=models.CASCADE)
    owner = models.CharField(max_length=20, blank=False)
    date_time = models.DateTimeField(auto_now=True)
    blog = models.TextField()
    #update_mileage = models.PositiveIntegerField()
    
    # Optional ... It might not have cost anything, might just be saying hey
    cost = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    # File for receipts
    
    # If you have a warranty, make it true, else it will be assumed there is no warranty for the entry
    # warranty = models.BooleanField(default=False)
    # Images

    def get_absolute_url(self):
        return reverse('entryDetail', args=[str(self.id)])
