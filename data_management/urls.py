# stream_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('stream_sensor_data/', views.stream_sensor_data, name='stream_sensor_data'), # 模拟生程数据
    path('save_to_db/', views.save_to_db,name='save_to_db'), #读取csv文件存入数据库
    # 从influxdb中读取一次实验的原始数据
    path('get_data/', views.get_data,name='get_data'),
    # 获取历史实验的tag
    path('get_history/', views.get_history, name='get_history'),
    # 新增一次实验
    path('create_new_exp/', views.create_new_exp, name='create_new_exp'),
]
