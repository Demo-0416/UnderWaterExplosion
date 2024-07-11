import json
import threading
import time
import numpy as np
from confluent_kafka import Producer
import pandas as pd

class DataSimulator:
    def __init__(self, params):
        self.params = params
        print(f"Initialized DataSimulator with params: {params}")

    def simulate_sensor_data(self, sensor_type, position, timestamp):
        noise_level = {'Pressure': 0.00001, 'Acceleration': 0.00001, 'Temperature': 0.00001, 'Strain': 0.00001}

        def generate_complex_noise(base_value, noise_level):
            noise = 0
            for _ in range(5):  # 叠加5个不同频率和幅度的波形
                frequency = np.random.uniform(0.1, 1.0)
                amplitude = np.random.uniform(0.1, 1.0) * noise_level
                phase = np.random.uniform(0, 2 * np.pi)
                noise += amplitude * np.sin(2 * np.pi * frequency * timestamp + phase)
            return noise

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

    def stream_sensor_data(self, positions, duration, kafka_topics):
        producers = {}
        for topic in kafka_topics:
            producers[topic] = Producer({'bootstrap.servers': 'localhost:9092'})

        def delivery_report(err, msg):
            if err is not None:
                print('Message delivery failed: {}'.format(err))
            else:
                print('Message delivered to {} [{}] {}'.format(msg.topic(), msg.partition(), msg.value()))

        def stream_data():
            time_array = np.arange(0, duration, 0.01)
            sensor_types = ['Acceleration', 'Strain', 'Temperature', 'Pressure']
            for timestamp in time_array:
                for location_index, position in enumerate(positions):
                    for i, sensor_type in enumerate(sensor_types):
                        sensor_id = location_index * 4 + i
                        sensor_data = self.simulate_sensor_data(sensor_type, position, timestamp)
                        record = {
                            'Time': timestamp,
                            'SensorID': sensor_id,
                            'Type': sensor_type,
                            'Position': position,
                            'Value': sensor_data  # Each record has only one data point
                        }
                        topic = kafka_topics[location_index]
                        producer = producers.get(topic)
                        if producer:
                            producer.produce(topic=topic, value=json.dumps(record), callback=delivery_report)
                for producer in producers.values():
                    producer.flush()
                # time.sleep(0.01)  # Ensure 0.01s interval between each data point

        threading.Thread(target=stream_data).start()

    def generate_explosive_events(self, positions, event_intervals):
        records = []
        sensor_types = ['Acceleration', 'Strain', 'Temperature', 'Pressure']
        for start, end in event_intervals:
            start_time = 0  # Start from 0 seconds
            end_time = (end - start) * 100  # Convert end time to 0.01s interval count
            time_array = np.arange(start_time, end_time, 0.01)
            for location_index, position in enumerate(positions):
                for i, sensor_type in enumerate(sensor_types):
                    sensor_id = location_index * 4 + i
                    for timestamp in time_array:
                        sensor_data = self.simulate_sensor_data(sensor_type, position, timestamp)
                        records.append({
                            'Time': timestamp,
                            'SensorID': sensor_id,
                            'Type': sensor_type,
                            'Position': position,
                            'Value': sensor_data
                        })
        return pd.DataFrame(records)

    def simulate_and_save_to_csv(self, positions, event_intervals, filename):
        df = self.generate_explosive_events(positions, event_intervals)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
