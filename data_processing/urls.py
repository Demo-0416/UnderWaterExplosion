from django.urls import path
from . import views

urlpatterns = [
    path('consume_sensor_data/', views.consume_sensor_data, name='consume_sensor_data'),# 消费数据，返回一个records
    path('extract_features/', views.extract_features_view, name='extract_features'),
    # path('plot_filtered_data/', views.plot_filtered_data, name='plot_filtered_data'),
]
