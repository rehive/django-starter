import datetime

from rest_framework.pagination import PageNumberPagination

ANONYMOUS_USER_ID = -1

CORS_ORIGIN_ALLOW_ALL = True

# REST FRAMEWORK ~ http://www.django-rest-framework.org/
# ---------------------------------------------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'EXCEPTION_HANDLER': 'config.exceptions.custom_exception_handler',
}

from rest_framework.settings import reload_api_settings
reload_api_settings(setting='REST_FRAMEWORK', value=REST_FRAMEWORK)
