import numpy as np
import pandas as pd


class DataSimulator:
    def __init__(self, params):
        self.params = params

    def simulate_sensor_data(self, sensor_type, position, time_array):
        global data
        noise_level = {'Pressure': 0.05, 'Acceleration': 0.1, 'Temperature': 0.5, 'Strain': 0.0001}
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
        return data

    def generate_all_sensors_data(self, num_sensors, positions, time_array):
        records = []
        for sensor_id in range(num_sensors):
            sensor_type = np.random.choice(['Pressure', 'Acceleration', 'Temperature', 'Strain'])
            position = positions[sensor_id]
            sensor_data = self.simulate_sensor_data(sensor_type, position, time_array)
            for i, value in enumerate(sensor_data):
                records.append({
                    'Time': time_array[i],
                    'SensorID': sensor_id,
                    'Type': sensor_type,
                    'Position': position,
                    'Value': value
                })
        return pd.DataFrame(records)


# 参数配置
params = {
    'P0': 1000, 'alpha': 0.1, 'nu': 0.05, 'omega': 2 * np.pi * 10, 'beta': 1,
    'T0': 20, 'DeltaT': 5, 'gamma': 0.05, 'phi': 2 * np.pi * 0.5, 'delta': 0.5,
    'epsilon0': 0.001, 'kappa': 0.1, 'psi': 2 * np.pi * 1, 'eta': 0.2
}

# 初始化模拟器
simulator = DataSimulator(params)

# 时间配置
t = np.linspace(0, 30 * 60, 30 * 60 * 100)

# 位置配置，每个位置固定有5个传感器
positions = np.tile(np.arange(20), 5)

# 生成所有传感器数据
df = simulator.generate_all_sensors_data(100, positions, t)

# 保存到CSV文件
df.to_csv('/mnt/data/SensorData.csv', index=False)
