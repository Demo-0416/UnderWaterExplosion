# stream_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stream_sensor_data/', views.stream_sensor_data, name='stream_sensor_data'),
    path('consume_sensor_data/', views.consume_sensor_data, name='consume_sensor_data'),
]
