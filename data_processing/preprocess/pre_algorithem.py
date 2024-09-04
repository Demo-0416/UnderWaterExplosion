# pre_process.py
import json
import threading
import time
import numpy as np
import pandas as pd
from confluent_kafka import Consumer, KafkaError
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import mpld3

def iir_filter(input_value, b, a, zi):
    """
    IIR滤波器

    参数:
    input_value - 输入值
    b, a - 滤波器系数
    zi - 初始状态

    返回:
    output_value - 经过滤波后的输出值
    zi - 更新后的状态
    """
    output_value, zi = signal.lfilter(b, a, [input_value], zi=zi)
    return output_value[0], zi


def fetch_data(consumer, max_messages=50000):
    # 初始化滤波器
    b, a = signal.butter(4, 0.3)  # 4阶Butterworth滤波器，截止频率为0.3
    zi_dict = {  # 使用字典来管理每种传感器的滤波器状态
        'Acceleration': signal.lfilter_zi(b, a) * 0,
        'Strain': signal.lfilter_zi(b, a) * 0,
        'Temperature': signal.lfilter_zi(b, a) * 0,
        'Pressure': signal.lfilter_zi(b, a) * 0
    }

    # 初始化数据结构
    records = {'Acceleration': [], 'Strain': [], 'Temperature': [], 'Pressure': []}
    raw_records = {'Acceleration': [], 'Strain': [], 'Temperature': [], 'Pressure': []}
    filtered_records = {'Acceleration': [], 'Strain': [], 'Temperature': [], 'Pressure': []}
    
    message_count = 0

    while message_count < max_messages:
        msg = consumer.poll(1.0)
        if msg is None:
            print("Waiting for new messages...")
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print("End of partition reached.")
                continue
            else:
                print(f"Error occurred: {msg.error()}")
                break

        # 处理接收到的消息
        record = json.loads(msg.value().decode('utf-8'))
        sensor_type = record.get('Type', None)
        value = record.get('Value', None)
        timestamp = record.get('Time', None)
        
        if value is not None and sensor_type in records:
            # 使用传感器类型特定的滤波器状态
            zi = zi_dict[sensor_type]
            filtered_value, zi = signal.lfilter(b, a, [value], zi=zi)
            zi_dict[sensor_type] = zi  # 更新滤波器状态

            raw_records[sensor_type].append((timestamp, value))
            filtered_records[sensor_type].append((timestamp, filtered_value[0]))
            records[sensor_type].append(record)
            print(f"Fetched and processed record: {record}")

        message_count += 1

    print("Reached maximum message count or encountered an error, stopping consumption.")
    processed_records = process_records(records)
    return processed_records

def process_records(records):
    processed = {}

    for sensor_type, sensor_data in records.items():
        processed[sensor_type] = []
        for record in sensor_data:
            sensor_id = record['SensorID']
            position = record['Position']
            time_value_pair = {'Time': record['Time'], 'Value': record['Value']}

            sensor_data_entry = next((item for item in processed[sensor_type] if item['SensorID'] == sensor_id), None)

            if not sensor_data_entry:
                sensor_data_entry = {
                    'SensorID': sensor_id,
                    'Type': sensor_type,
                    'Position': position,
                    'X-axis-name': 'Time',
                    'Y-axis-name': 'Value',
                    'data': []
                }
                processed[sensor_type].append(sensor_data_entry)

            sensor_data_entry['data'].append(time_value_pair)

    return processed
def generate_plots(records):
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    sensor_types = ['Acceleration', 'Strain', 'Temperature', 'Pressure']
    # 选择第一个和最后一个位置
    positions_of_interest = {100, 1000}
    colors = plt.cm.viridis(np.linspace(0, 1, len(positions_of_interest)))

    for i, sensor_type in enumerate(sensor_types):
        ax = axs[i // 2, i % 2]
        sensor_data = records[sensor_type]
        locations = set([record['Position'] for record in sensor_data if record['Position'] in positions_of_interest])
        
        for j, location in enumerate(locations):
            location_data = [(record['Time'], record['Value']) for record in sensor_data if record['Position'] == location]
            if location_data:
                times, values = zip(*location_data)
                ax.plot(times, values, label=f'Location {location}', color=colors[j])
        
        ax.set_title(sensor_type)
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.legend()
        ax.grid(True)

    plt.tight_layout()
    return mpld3.fig_to_html(fig)