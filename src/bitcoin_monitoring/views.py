from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from bitcoin_monitoring.models import Webhook
from bitcoin_monitoring.serializers import WebhookSerializer

from logging import getLogger

logger = getLogger('django')


class WebhookView(CreateAPIView):
    allowed_methods = ('POST',)
    permission_classes = (AllowAny,)
    serializer_class = WebhookSerializer