# data_processing/feature_extraction.py

import numpy as np

def extract_features(processed_records):
    """
    从处理后的数据中提取特征。

    参数:
    processed_records - 处理后的数据字典

    返回:
    features - 包含提取特征的字典
    """
    features = {}

    for sensor_type, sensor_data_list in processed_records.items():
        features[sensor_type] = []
        for sensor_data in sensor_data_list:
            sensor_id = sensor_data['SensorID']
            values = [data_point['Value'] for data_point in sensor_data['data']]

            # 提取特征
            mean_value = np.mean(values)
            max_value = np.max(values)
            min_value = np.min(values)
            std_dev = np.std(values)
            peak_to_peak = max_value - min_value

            feature_dict = {
                'SensorID': sensor_id,
                'Mean': mean_value,
                'Max': max_value,
                'Min': min_value,
                'StdDev': std_dev,
                'PeakToPeak': peak_to_peak
            }

            features[sensor_type].append(feature_dict)

    return features
