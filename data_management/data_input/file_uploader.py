import pandas as pd
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

def read_csv(file_path):
    """读取 CSV 文件并返回数据帧"""
    return pd.read_csv(file_path)



def read_csv_and_write_to_influxdb(csv_file_path, influxdb_url, token, org, bucket):
    # 读取 CSV 文件
    df = pd.read_csv(csv_file_path)
    
    # 确保时间列转换为 datetime 对象
    df['Time'] = pd.to_datetime(df['Time'])
    
    # 初始化 InfluxDB 客户端
    client = InfluxDBClient(url=influxdb_url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    # 将 DataFrame 中的数据写入 InfluxDB
    for index, row in df.iterrows():
        point = Point("measurement_name").time(row['Time'])  # 替换为你的测量名称
        point = point.tag("SensorID", row['SensorID'])  # 添加 SensorID 作为标签
        point = point.field("Type", row['Type'])
        point = point.field("Position", row['Position'])
        point = point.field("Value", row['Value'])
        
        write_api.write(bucket=bucket, org=org, record=point)
    
    # 关闭客户端
    client.close()

# 使用示例
csv_file_path = 'E:/PythonMyTest/test_data.csv'
influxdb_url = 'http://localhost:8086'
token = '69BT3gXrJx_XQmR91PmIBcDlPbnUFGTRZ-YkQIcG7gg04PHPEqGNyJwxOMipsdfSLpusMdoDP7OjAjJIjIEZ4A=='
org = 'Data'
bucket = 'CsvTest'

read_csv_and_write_to_influxdb(csv_file_path, influxdb_url, token, org, bucket)
