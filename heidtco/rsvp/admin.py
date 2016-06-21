from django.contrib import admin

from . import models
# Register your models here.

class RSVPAdmin(admin.ModelAdmin):
    list_display = ('modified', 'email', 'rsvp', 'details')
    readonly_fields = ('first_seen', 'created', 'uuid', 'client_id')

    ordering = ('-modified',)

admin.site.register(models.RSVP, RSVPAdmin)
