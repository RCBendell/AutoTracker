from django.contrib import admin

# Register your models here.

from .models import car, entry, reminder

class carAdmin(admin.ModelAdmin):
    list_display = ('owner', 'make', 'model', 'year', 'image')
admin.site.register(car, carAdmin)

class entryAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'modified_date_time', 'owner', 'car', 'cost', 'image1', 'image2')
admin.site.register(entry, entryAdmin)

class reminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'car', 'remind_on_date')
admin.site.register(reminder, reminderAdmin)