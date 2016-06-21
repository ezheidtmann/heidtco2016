from __future__ import unicode_literals

from django.db import models

import common.models

class RSVP(common.models.AutoDateModel):
    uuid = models.UUIDField(primary_key=True)

    client_id = models.UUIDField()

    rsvp = models.NullBooleanField()
    details = models.TextField(default='')
    email = models.CharField(max_length=255, blank=True, default='')
    STATUS_IN_PROGRESS = 'in-progress'
    STATUS_COMPLETE = 'complete'
    STATUS_CHOICES = (
        (STATUS_IN_PROGRESS, STATUS_IN_PROGRESS),
        (STATUS_COMPLETE, STATUS_COMPLETE),
    )
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=STATUS_IN_PROGRESS)

# Create your models here.
