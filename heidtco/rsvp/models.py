from __future__ import unicode_literals

from django.db import models

import common.models

class RSVP(common.models.AutoDateModel):
    uuid = models.UUIDField(primary_key=True)

    client_id = models.UUIDField()

    rsvp = models.NullBooleanField()
    details = models.TextField(default='')
    email = models.CharField(max_length=255, blank=True, default='')

# Create your models here.
