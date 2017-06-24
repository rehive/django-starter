from logging import getLogger

import datetime
from uuid import uuid4

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.timezone import utc

logger = getLogger('django')

class Message(models.Model):
    first_name = models.CharField(max_length=300, null=True, blank=True)
    last_name = models.CharField(max_length=300, null=True, blank=True)
    message = models.CharField(max_length=300, null=False, blank=False)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    def __str__(self):
        return str(self.id)


    def save(self, *args, **kwargs):
        if not self.id:  # On create
            self.created = datetime.datetime.now(tz=utc)

        self.updated = datetime.datetime.now(tz=utc)
        return super(Message, self).save(*args, **kwargs)


