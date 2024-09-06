import json
import threading
import time
import os
import numpy as np
from confluent_kafka import Producer
import pandas as pd
from data_management.setting import csv_file_path
from data_management.data_input.file_uploader import DataSaver
from data_management.data_input.file_uploader import FollowExp

# 定义一个名为 DataSimulator 的类
class DataSimulator:
    # 类的初始化方法，接收参数 params
    def __init__(self, params):
        self.params = params
        # 打印初始化信息
        print(f"Initialized DataSimulator with params: {params}")

    # 模拟传感器数据的方法，接收传感器类型、位置和时间戳作为参数
    def simulate_sensor_data(self, sensor_type, position, timestamp):
        # 不同传感器类型的噪声水平字典
        noise_level = {'Pressure': 0.00001, 'Acceleration': 0.00001, 'Temperature': 0.00001, 'Strain': 0.00001}

        # 定义生成复杂噪声的内部函数
        def generate_complex_noise(base_value, noise_level):
            noise = 0
            # 叠加 5 个不同频率和幅度的波形来生成噪声
            for _ in range(5):
                frequency = np.random.uniform(0.1, 1.0)
                amplitude = np.random.uniform(0.1, 1.0) * noise_level
                phase = np.random.uniform(0, 2 * np.pi)
                noise += amplitude * np.sin(2 * np.pi * frequency * timestamp + phase)
            return noise

        # 根据传感器类型生成不同的基础数据，并添加噪声
        if sensor_type == 'Pressure':
            base_data = self.params['P0'] * np.exp(
                -self.params['alpha'] * position - self.params['nu'] * timestamp) * np.cos(
                self.params['omega'] * timestamp - self.params['beta'] * position)
            noise = generate_complex_noise(base_data, noise_level['Pressure'] * self.params['P0'])
        elif sensor_type == 'Acceleration':
            base_data = -self.params['alpha'] * self.params['P0'] * np.exp(-self.params['alpha'] * position) * np.sin(
                self.params['omega'] * timestamp - self.params['beta'] * position)
            noise = generate_complex_noise(base_data, noise_level['Acceleration'] * abs(base_data))
        elif sensor_type == 'Temperature':
            base_data = self.params['T0'] + self.params['DeltaT'] * np.exp(-self.params['gamma'] * position) * np.cos(
                self.params['phi'] * timestamp - self.params['delta'] * position)
            noise = generate_complex_noise(base_data, noise_level['Temperature'])
        elif sensor_type == 'Strain':
            base_data = self.params['epsilon0'] * np.exp(-self.params['kappa'] * position) * np.cos(
                self.params['psi'] * timestamp - self.params['eta'] * position)
            noise = generate_complex_noise(base_data, noise_level['Strain'])
        data = base_data + noise
        return data

    # 流式传输传感器数据的方法，接收位置列表、爆炸持续时间、Kafka 主题列表、爆炸次数、年份和实验名称作为参数
    def stream_sensor_data(self, positions, explosion_duration, kafka_topics, num_explosions, year, exp_name):
        producers = {}
        # 为每个 Kafka 主题创建一个生产者实例
        for topic in kafka_topics:
            producers[topic] = Producer({'bootstrap.servers': 'localhost:9092'})

        # 定义消息发送的回调函数，用于处理发送错误
        def delivery_report(err, msg):
            if err is not None:
                print('Message delivery failed: {}'.format(err))

        # 定义流式传输数据的内部函数
        def stream_data():
            # 创建每个爆炸持续时间的时间数组
            time_array = np.arange(0, explosion_duration, 0.01)
            sensor_types = ['Acceleration', 'Strain', 'Temperature', 'Pressure']
            explosion_interval = 30  # 每次爆炸之间的间隔
            records = []  # 用于保存所有生成的数据记录

            # 模拟多次爆炸的数据生成
            for explosion in range(num_explosions):
                explosion_start_time = explosion * (explosion_duration + explosion_interval)
                for location_index, position in enumerate(positions):
                    for i, sensor_type in enumerate(sensor_types):
                        sensor_id = location_index * 4 + i  # 每个位置有 4 个传感器类型，从 0 开始
                        for t in time_array:
                            timestamp = explosion_start_time + t
                            sensor_data = self.simulate_sensor_data(sensor_type, position, np.array([t]))[0]
                            record = {
                                'Time': float(timestamp),
                                'SensorID': int(sensor_id),
                                'Type': sensor_type,
                                'Position': float(position),
                                'Value': float(sensor_data)  # 单个数据点
                            }
                            records.append(record)  # 将记录加入列表

                            # 发送数据到 Kafka 主题（如果需要保留 Kafka 发送功能）
                            topic = kafka_topics[location_index]
                            producer = producers.get(topic)
                            if producer:
                                producer.produce(topic=topic, value=json.dumps(record), callback=delivery_report)

                for producer in producers.values():
                    producer.flush()

            # 保存数据到 CSV 文件
            filename = f"{year}_{exp_name}_sensor_data.csv"
            save_directory = csv_file_path
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            save_path = os.path.join(save_directory, filename)
            df = pd.DataFrame(records)
            df.to_csv(save_path, index=False)
            print(f"Data saved to {filename}")
            # 创建历史记录
            FollowExp().create_history(year, exp_name,'ori')
            # 将数据保存到数据库
            DataSaver().read_csv_and_write_to_influxdb(year, exp_name)
            print(f"Data saved to db")

        stream_data()