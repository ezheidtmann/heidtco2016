from django.db import models

def utcnow():
    import datetime
    import pytz
    d = datetime.datetime.utcnow()
    d = d.replace(tzinfo=pytz.utc)
    return d

class AutoDateModel(models.Model):
    first_seen = models.DateTimeField(default=utcnow)
    created = models.DateTimeField(default=utcnow)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
