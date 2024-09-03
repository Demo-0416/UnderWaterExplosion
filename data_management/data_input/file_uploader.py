import pandas as pd
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from data_management.setting import settings
from data_management.setting import csv_file_path
from data_management import models






class DataSaver:
    def save_exp_tag(self, year, exp_name):
        try:
            exp_tag = models.History(save_time=year, exp_name=exp_name)
            exp_tag.save()
        except Exception as e:
            return str(e)

    def read_csv_and_write_to_influxdb(self, year, exp_name):
        client = InfluxDBClient(**settings)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        measurement = year + '_' + exp_name + '_ori'
        cur_csv_file_path = csv_file_path + year + exp_name + 'sensor_data.csv'
        # 读取 CSV 文件并将数据写入 InfluxDB
        df = pd.read_csv(cur_csv_file_path)
        for index, row in df.iterrows():
            point = Point(measurement)  # 替换为你的测量名称
            point = point.tag("SensorID", row['SensorID'])  # 添加 SensorID 作为标签
            point = point.tag("Type", row['Type'])
            point = point.field("Position", row['Position'])
            point = point.field("Value", row['Value'])
            point = point.field("Time", row['Time'])  # 添加时间戳

            # 写入 InfluxDB
            write_api.write(bucket=settings['bucket'], org=settings['org'], record=point)
    
        # 关闭 InfluxDB 客户端
        client.close()
        self.save_exp_tag(year, exp_name)
