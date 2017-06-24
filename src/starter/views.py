from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from .serializers import MessageSerializer
from .models import Message

from logging import getLogger

logger = getLogger('django')

class MessageView(ListCreateAPIView):
    allowed_methods = ('POST',)
    permission_classes = (AllowAny,)
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
