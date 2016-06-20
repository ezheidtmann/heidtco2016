from django.contrib import admin

from . import models
# Register your models here.

class RSVPAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.RSVP, RSVPAdmin)
