import numpy as np
import pandas as pd

class DataSimulator:
    def __init__(self, params):
        self.params = params
        print(f"Initialized DataSimulator with params: {params}")

    def simulate_sensor_data(self, sensor_type, position, time_array):
        global data
        print(f"Simulating {sensor_type} data at position {position} for time array of length {len(time_array)}")
        noise_level = {'Pressure': 0.00001, 'Acceleration': 0.00001, 'Temperature': 0.00001, 'Strain': 0.00001}
        if sensor_type == 'Pressure':
            base_data = self.params['P0'] * np.exp(
                -self.params['alpha'] * position - self.params['nu'] * time_array) * np.cos(
                self.params['omega'] * time_array - self.params['beta'] * position)
            noise = np.random.normal(0, noise_level['Pressure'] * self.params['P0'], base_data.shape)
            data = base_data + noise
        elif sensor_type == 'Acceleration':
            base_data = -self.params['alpha'] * self.params['P0'] * np.exp(-self.params['alpha'] * position) * np.sin(
                self.params['omega'] * time_array - self.params['beta'] * position)
            noise = np.random.normal(0, noise_level['Acceleration'] * abs(base_data), base_data.shape)
            data = base_data + noise
        elif sensor_type == 'Temperature':
            base_data = self.params['T0'] + self.params['DeltaT'] * np.exp(-self.params['gamma'] * position) * np.cos(
                self.params['phi'] * time_array - self.params['delta'] * position)
            noise = np.random.normal(0, noise_level['Temperature'], base_data.shape)
            data = base_data + noise
        elif sensor_type == 'Strain':
            base_data = self.params['epsilon0'] * np.exp(-self.params['kappa'] * position) * np.cos(
                self.params['psi'] * time_array - self.params['eta'] * position)
            noise = np.random.normal(0, noise_level['Strain'], base_data.shape)
            data = base_data + noise
        print(f"Generated data for {sensor_type} at position {position}: {data[:5]}...")  # Show first 5 data points for brevity
        return data

    def generate_explosive_events(self, num_sensors, positions, time_array, event_intervals):
        records = []
        for start, end in event_intervals:
            print(f"Generating data for event from {start} to {end} seconds")
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
        print(f"Generated {len(records)} records for all events")
        return pd.DataFrame(records)

# 参数配置
params = {
    'P0': 1000, 'alpha': 0.1, 'nu': 0.05, 'omega': 2 * np.pi * 10, 'beta': 1,
    'T0': 20, 'DeltaT': 5, 'gamma': 0.05, 'phi': 2 * np.pi * 0.5, 'delta': 0.5,
    'epsilon0': 0.001, 'kappa': 0.1, 'psi': 2 * np.pi * 1, 'eta': 0.2
}
print("Simulation parameters set.")

# 初始化模拟器
simulator = DataSimulator(params)

# 时间配置
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

# 生成所有传感器数据
df = simulator.generate_explosive_events(100, positions, t, event_intervals)

# 保存到CSV文件
df.to_csv('SensorData.csv', index=False)
print("Sensor data saved to SensorData.csv.")
