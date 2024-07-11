# stream_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stream_sensor_data/', views.stream_sensor_data, name='stream_sensor_data'),
    path('save_sensor_data/',views.save_sensor_data,name='save_sensor_data'),
    path('save_to_db',views.save_to_db,name='save_to_db'),
]
