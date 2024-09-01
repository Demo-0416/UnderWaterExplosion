# stream_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('stream_sensor_data/', views.stream_sensor_data, name='stream_sensor_data'), # 模拟生程数据
    path('save_sensor_data/',views.save_sensor_data,name='save_sensor_data'), #保存模拟数据为csv文件
    path('save_to_db/',views.save_to_db,name='save_to_db'), #读取csv文件存入数据库
    # 从influxdb中读取一次实验的原始数据
    path('get_ori_data/', views.get_ori_data,name='get_ori_data'),
]
