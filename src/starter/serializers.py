from logging import getLogger

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from starter.models import Message

logger = getLogger('django')


class MessageSerializer(ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    message = serializers.CharField(required=True)

    class Meta:
        model = Message
        fields = ('first_name', 'last_name', 'message')

