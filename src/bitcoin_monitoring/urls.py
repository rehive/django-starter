from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = (
    url(r'^webhooks/$', views.WebhookView.as_view(), name='webhooks'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
