# your_app_name/routing.py
from django.urls import re_path
from .websocket import SensorDataConsumer

websocket_urlpatterns = [
    re_path(r'ws/sensor_data/$', SensorDataConsumer.as_asgi()),
]
