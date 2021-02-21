from django.contrib import admin

# Register your models here.

from .models import car

# admin.site.register(car)
class carAdmin(admin.ModelAdmin):
    list_display = ('owner', 'make', 'model', 'year')
admin.site.register(car, carAdmin)