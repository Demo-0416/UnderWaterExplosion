import pandas as pd
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class DataSaver:

 def read_csv_and_write_to_influxdb(csv_file_path, influxdb_url, token, org, bucket):
    # 初始化 InfluxDB 客户端
    client = InfluxDBClient(url=influxdb_url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    # 读取 CSV 文件并将数据写入 InfluxDB
    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        point = Point("measurement_name")  # 替换为你的测量名称
        point = point.tag("SensorID", row['SensorID'])  # 添加 SensorID 作为标签
        point = point.tag("Type", row['Type'])
        point = point.field("Position", row['Position'])
        point = point.field("Value", row['Value'])
        point = point.field("Time", row['Time'])  # 添加时间戳
        
        # 写入 InfluxDB
        write_api.write(bucket=bucket, org=org, record=point)
    
    # 关闭 InfluxDB 客户端
    client.close()

# 使用示例
csv_file_path = 'E:/2024XXQ/UnderWaterExplosion/SensorData.csv'
influxdb_url = 'http://localhost:8086'
token = 'DugaItJRzzLbbNgUrEuoWxv84iIE8LS68eNUhuXgRKrzabA62vIBfqn9H2LhIyACArjqEKG1t7b2CXY5gyDP7A=='
org = 'Data'
bucket = 'Csv'