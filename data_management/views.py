# stream_app/views.py
from django.http import JsonResponse
from django.shortcuts import render
import numpy as np
import threading
from .data_input.data_simulator import DataSimulator
from .data_input.file_uploader import DataSaver

# 参数配置
params_simulator = {
    'P0': 1000, 'alpha': 0.1, 'nu': 0.05, 'omega': 2 * np.pi * 10, 'beta': 1,
    'T0': 20, 'DeltaT': 5, 'gamma': 0.05, 'phi': 2 * np.pi * 0.5, 'delta': 0.5,
    'epsilon0': 0.001, 'kappa': 0.1, 'psi': 2 * np.pi * 1, 'eta': 0.2
}

# 初始化模拟器
simulator = DataSimulator(params_simulator)
data_saver=DataSaver
def stream_sensor_data(request):
    if request.method == 'GET':
        positions = np.linspace(100, 1000, 25)  # 生成 25 个位置
        kafka_topics = [f'location_{i}_data_topic' for i in range(1, 26)]
        
        # 启动数据流线程
        threading.Thread(target=simulator.stream_sensor_data, args=(positions, 60, kafka_topics)).start()
        
        return JsonResponse({'status': 'streaming started'})

def home(request):
    return render(request, 'data_management/home.html')

positions = np.linspace(100, 1000, 25)  # 生成 25 个位置，每个位置的值是整数
duration = 1  # 持续时间 1 秒
filename = "sensor_data.csv"
num_explosions = 5  # 爆炸次数
def save_sensor_data(request):
    if request.method == 'GET':
        # 调用 save_sensor_data 方法保存数据到 CSV 文件
        simulator.save_sensor_data(positions, duration, filename, num_explosions)
    return JsonResponse({'status': 'save completed'})
    
csv_file_path = 'E:/2024XXQ/UnderWaterExplosion/SensorData.csv'
influxdb_url = 'http://localhost:8086'
token = 'DugaItJRzzLbbNgUrEuoWxv84iIE8LS68eNUhuXgRKrzabA62vIBfqn9H2LhIyACArjqEKG1t7b2CXY5gyDP7A=='
org = 'Data'
bucket = 'Csv'
def save_to_db(request):
    if request.method=='GET':
        data_saver.read_csv_and_write_to_influxdb(csv_file_path, influxdb_url, token, org, bucket)
    return JsonResponse({'status':'save to database'})