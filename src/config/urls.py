from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import (
    password_reset_complete, password_reset_confirm)

from . import views

import debug_toolbar

admin.autodiscover()

urlpatterns = (
    # Views
    url(r'^', include('bitcoin_monitoring.urls', namespace='bitcoin-monitoring')),
)

# Add debug URL routes
if settings.DEBUG:
    urlpatterns = (
        url(r'^$', views.index, name='index'),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ) + urlpatterns
