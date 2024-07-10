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

    def simulate_sensor_data(self, sensor_type, position, time_array):
        global base_data, noise
        noise_level = {'Pressure': 0.00001, 'Acceleration': 0.00001, 'Temperature': 0.00001, 'Strain': 0.00001}

        def generate_complex_noise(base_shape, noise_level):
            noise = np.zeros(base_shape)
            for _ in range(5):  # 叠加5个不同频率和幅度的波形
                frequency = np.random.uniform(0.1, 1.0)
                amplitude = np.random.uniform(0.1, 1.0) * noise_level
                phase = np.random.uniform(0, 2 * np.pi)
                noise += amplitude * np.sin(2 * np.pi * frequency * time_array + phase)
            return noise

        if sensor_type == 'Pressure':
            base_data = self.params['P0'] * np.exp(
                -self.params['alpha'] * position - self.params['nu'] * time_array) * np.cos(
                self.params['omega'] * time_array - self.params['beta'] * position)
            noise = generate_complex_noise(base_data.shape, noise_level['Pressure'] * self.params['P0'])
        elif sensor_type == 'Acceleration':
            base_data = -self.params['alpha'] * self.params['P0'] * np.exp(-self.params['alpha'] * position) * np.sin(
                self.params['omega'] * time_array - self.params['beta'] * position)
            noise = generate_complex_noise(base_data.shape, noise_level['Acceleration'] * abs(base_data))
        elif sensor_type == 'Temperature':
            base_data = self.params['T0'] + self.params['DeltaT'] * np.exp(-self.params['gamma'] * position) * np.cos(
                self.params['phi'] * time_array - self.params['delta'] * position)
            noise = generate_complex_noise(base_data.shape, noise_level['Temperature'])
        elif sensor_type == 'Strain':
            base_data = self.params['epsilon0'] * np.exp(-self.params['kappa'] * position) * np.cos(
                self.params['psi'] * time_array - self.params['eta'] * position)
            noise = generate_complex_noise(base_data.shape, noise_level['Strain'])
        data = base_data + noise
        print(
            f"Generated data for {sensor_type} at position {position}: {data[:5]}...")  # Show first 5 data points for brevity
        return data

    def stream_sensor_data(self, num_sensors, positions, duration, kafka_topics):
        producers = {}
        for sensor_type, topic in kafka_topics.items():
            producers[sensor_type] = Producer({'bootstrap.servers': 'localhost:9092'})

        def delivery_report(err, msg):
            if err is not None:
                print('Message delivery failed: {}'.format(err))
            else:
                print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

        def stream_data():
            time_array = np.linspace(0, 1, 100)
            end_time = time.time() + duration
            while time.time() < end_time:
                for sensor_id in range(num_sensors):
                    sensor_type = np.random.choice(['Pressure', 'Acceleration', 'Temperature', 'Strain'])
                    position = positions[sensor_id]
                    sensor_data = self.simulate_sensor_data(sensor_type, position, time_array)
                    record = {
                        'Time': time.time(),
                        'SensorID': sensor_id,
                        'Type': sensor_type,
                        'Position': position,
                        'Value': sensor_data.tolist()  # Convert to list for JSON serialization
                    }
                    producer = producers.get(sensor_type)
                    if producer:
                        producer.produce(topic=kafka_topics[sensor_type], value=json.dumps(record),
                                         callback=delivery_report)
                for producer in producers.values():
                    producer.flush()
                time.sleep(1)

        streaming_thread = threading.Thread(target=stream_data)
        streaming_thread.start()

    def generate_explosive_events(self, num_sensors, positions, time_array, event_intervals):
        records = []
        for start, end in event_intervals:
            for sensor_id in range(num_sensors):
                sensor_type = np.random.choice(['Pressure', 'Acceleration', 'Temperature', 'Strain'])
                position = positions[sensor_id]
                event_time_array = time_array[(time_array >= start) & (time_array <= end)]
                sensor_data = self.simulate_sensor_data(sensor_type, position, event_time_array)
                for i, value in enumerate(sensor_data):
                    records.append({
                        'Time': np.float64(event_time_array[i]),
                        'SensorID': sensor_id,
                        'Type': sensor_type,
                        'Position': position,
                        'Value': value
                    })
        return pd.DataFrame(records)

    def simulate_and_save_to_csv(self, num_sensors, positions, time_array, event_intervals, filename):
        df = self.generate_explosive_events(num_sensors, positions, time_array, event_intervals)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
