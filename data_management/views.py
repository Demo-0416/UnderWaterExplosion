# stream_app/views.py
from django.http import JsonResponse
from django.shortcuts import render
import numpy as np
import threading
from confluent_kafka import Consumer, KafkaError
from .data_input.data_simulator import DataSimulator

# 参数配置
params = {
    'P0': 1000, 'alpha': 0.1, 'nu': 0.05, 'omega': 2 * np.pi * 10, 'beta': 1,
    'T0': 20, 'DeltaT': 5, 'gamma': 0.05, 'phi': 2 * np.pi * 0.5, 'delta': 0.5,
    'epsilon0': 0.001, 'kappa': 0.1, 'psi': 2 * np.pi * 1, 'eta': 0.2
}

# 初始化模拟器
simulator = DataSimulator(params)

def stream_sensor_data(request):
    if request.method == 'GET':
        positions = np.tile(np.linspace(100, 1050, 20), 5)
        kafka_topic = 'sensor_data'
        
        # 启动数据流线程
        threading.Thread(target=simulator.stream_sensor_data, args=(100, positions, 60, kafka_topic)).start()
        
        return JsonResponse({'status': 'streaming started'})

def consume_sensor_data(request):
    if request.method == 'GET':
        records = []
        consumer = Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'sensor_data_group',
            'auto.offset.reset': 'earliest'
        })
        consumer.subscribe(['sensor_data'])
        
        def fetch_data():
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break
                record = msg.value().decode('utf-8')
                print(f"Consumed record: {record}")  # 打印消费者信息到控制台
                records.append(record)
        
        threading.Thread(target=fetch_data).start()
        return JsonResponse({'status': 'consuming started', 'records': records})
    
def home(request):
    return render(request, 'data_management/home.html')
total_duration = 5 * 60  # 5分钟
t = np.linspace(0, total_duration, total_duration * 100)
print(f"Time array generated with {len(t)} points.")

# 位置配置，每个位置固定有5个传感器
positions = np.tile(np.linspace(100, 1050, 20), 5)
print(f"Positions array generated with {len(positions)} positions.")

# 定义事件间隔，每次起爆持续30秒，共10次
event_duration = 30
num_events = 10
event_intervals = [(i * event_duration, (i + 1) * event_duration) for i in range(num_events)]
print(f"Event intervals defined: {event_intervals}")
def save_sensor_data(request):
    if request.method == 'GET':
     simulator.simulate_and_save_to_csv(100, positions, t, event_intervals, 'SensorData.csv')
    
