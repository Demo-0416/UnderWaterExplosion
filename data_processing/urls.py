from django.urls import path
from . import views

urlpatterns = [
    path('consume_sensor_data/', views.consume_sensor_data, name='consume_sensor_data'),
    path('plot_filtered_data/', views.plot_filtered_data, name='plot_filtered_data'),
]
