from django.contrib import admin

# Register your models here.

from .models import car, entry

# admin.site.register(car)
class carAdmin(admin.ModelAdmin):
    list_display = ('owner', 'make', 'model', 'year')
admin.site.register(car, carAdmin)

class entryAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time', 'owner', 'car', 'cost')
admin.site.register(entry, entryAdmin)