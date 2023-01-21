from django.urls import path
from .views import WebhookInterface


urlpatterns = [
    path('webhook',WebhookInterface.as_view(),name='webhook')
]