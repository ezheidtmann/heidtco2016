from django.contrib import admin

from . import models
# Register your models here.

class RSVPAdmin(admin.ModelAdmin):
    list_display = ('rsvp', 'email', 'details')

admin.site.register(models.RSVP, RSVPAdmin)
