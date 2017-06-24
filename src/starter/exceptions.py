from rest_framework import status
from django.utils.encoding import force_text
from rest_framework.exceptions import APIException


class NotImplementedAPIError(APIException):
    status_code = 501
    default_detail = 'Functionality not implemented.'


class StarterError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'
    default_error_slug = 'internal_error'

    def __init__(self, detail=None, error_slug=None):
        if detail is not None:
            self.detail = force_text(detail)
            self.error_slug = force_text(error_slug)
        else:
            self.detail = force_text(self.default_detail)
            self.error_slug = force_text(self.default_error_slug)

    def __str__(self):
        return self.detail

