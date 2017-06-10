from logging import getLogger

import datetime
from uuid import uuid4

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.timezone import utc

from bitcoin_monitoring.api import BitcoinMonitoringInterface

logger = getLogger('django')


class Webhook(models.Model):
    url = models.URLField(max_length=300, null=False, blank=False,)
    address = models.CharField(max_length=300, null=False, blank=False, db_index=True)
    last_block = models.IntegerField(null=True, blank=True)
    confirmations = models.IntegerField(null=True, blank=True, default=6)
    metadata = JSONField(null=True, blank=True, default=dict)
    secret = models.CharField(max_length=300, null=True, blank=True)
    webhook_id = models.CharField(max_length=200, null=True, db_index=True, unique=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    def __str__(self):
        return str(self.address)

    def save(self, *args, **kwargs):
        if not self.id:  # On create
            interface = BitcoinMonitoringInterface()
            block_height = interface.get_block_height()
            self.last_block = block_height  # Only subscribe to new transaction notifications
            self.created = datetime.datetime.now(tz=utc)
            self.webhook_id = str(uuid4())

        self.updated = datetime.datetime.now(tz=utc)
        return super(Webhook, self).save(*args, **kwargs)


class Transaction(models.Model):
    """
    Third-party transaction model. Includes methods for creating/ confirming on Rehive and for executing with the
    third-party.
    """
    STATUS = (
        ('Processing', 'Processing'),
        ('Error', 'Error'),
        ('Complete', 'Complete'),
    )
    tx_code = models.CharField(max_length=200, null=True, db_index=True)
    address = models.CharField(max_length=300, null=False, blank=False)
    data = JSONField(null=True, blank=True, default=dict)
    confirmations = models.IntegerField(null=True, blank=True, db_index=True)
    notifications = models.IntegerField(null=True, blank=True, db_index=True)  # number of webhooks already sent
    response = JSONField(null=True, blank=True, default=dict)
    response_code = models.CharField(max_length=5, null=True)
    webhook = models.ForeignKey(Webhook, null=True, blank=True)
    status = models.CharField(max_length=24, choices=STATUS, null=True, blank=True, db_index=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        unique_together = (("tx_code", "webhook"),)

    def save(self, *args, **kwargs):
        if not self.id:  # On create
            self.created = datetime.datetime.now(tz=utc)

        self.updated = datetime.datetime.now(tz=utc)
        return super(Transaction, self).save(*args, **kwargs)


