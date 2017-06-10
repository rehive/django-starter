from logging import getLogger

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from bitcoin_monitoring.models import Webhook

logger = getLogger('django')


class WebhookSerializer(ModelSerializer):
    url = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    confirmations = serializers.IntegerField(required=False)
    secret = serializers.CharField(required=True, write_only=True)
    webhook_id = serializers.CharField(read_only=True)

    class Meta:
        model = Webhook
        fields = ('url', 'webhook_id', 'address', 'confirmations', 'secret')

