from django.contrib import admin

from import_export import resources
import import_export.admin

from . import models

class RSVPResource(resources.ModelResource):
    class Meta:
        model = models.RSVP
        import_id_fields = ('uuid',)
        fields = ('uuid', 'created', 'modified', 'email', 'rsvp', 'details')

class RSVPAdmin(import_export.admin.ExportMixin, admin.ModelAdmin):
    resource_class = RSVPResource

    list_display = ('modified', 'status', 'email', 'rsvp', 'details')
    readonly_fields = ('first_seen', 'created', 'uuid', 'client_id')

    ordering = ('-modified',)

admin.site.register(models.RSVP, RSVPAdmin)
