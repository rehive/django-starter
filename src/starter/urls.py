from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = (
    url(r'^messages/$', views.MessageView.as_view(), name='messages'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
