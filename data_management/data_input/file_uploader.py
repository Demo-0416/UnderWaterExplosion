import pandas as pd
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from kafka import KafkaProducer, KafkaConsumer
import json
from threading import Thread
import time

def read_csv(file_path):
    """读取 CSV 文件并返回数据帧"""
    return pd.read_csv(file_path)

def produce_to_kafka(producer, topic, message):
    producer.send(topic, value=message)
    producer.flush()

def consume_from_kafka(consumer):
    for message in consumer:
        print(f"Received message: {message.value}")

def kafka_producer_thread(csv_file_path, kafka_bootstrap_servers, kafka_topic):
    # 读取 CSV 文件
    df = pd.read_csv(csv_file_path)
    
    # 初始化 Kafka 生产者
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    
    # 将 DataFrame 中的数据发送到 Kafka
    for index, row in df.iterrows():
        message = {
            "SensorID": row['SensorID'],
            "Type": row['Type'],
            "Position": row['Position'],
            "Value": row['Value'],
            "Time": row['Time']
        }
        produce_to_kafka(producer, kafka_topic, message)
        time.sleep(0.01)  # 模拟延迟
    
    # 关闭生产者
    producer.close()

def kafka_consumer_thread(kafka_bootstrap_servers, kafka_topic):
    # 初始化 Kafka 消费者
    consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_bootstrap_servers, auto_offset_reset='earliest', value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    consume_from_kafka(consumer)

def read_csv_and_write_to_influxdb_and_kafka(csv_file_path, influxdb_url, token, org, bucket, kafka_bootstrap_servers, kafka_topic):
    # 初始化 InfluxDB 客户端
    client = InfluxDBClient(url=influxdb_url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    # 启动 Kafka 生产者线程
    producer_thread = Thread(target=kafka_producer_thread, args=(csv_file_path, kafka_bootstrap_servers, kafka_topic))
    producer_thread.start()
    
    # 启动 Kafka 消费者线程
    consumer_thread = Thread(target=kafka_consumer_thread, args=(kafka_bootstrap_servers, kafka_topic))
    consumer_thread.start()
    
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
    
    # 等待线程完成
    producer_thread.join()
    consumer_thread.join()
    
    # 关闭 InfluxDB 客户端
    client.close()

# 使用示例
csv_file_path = 'E:/2024XXQ/UnderWaterExplosion/SensorData.csv'
influxdb_url = 'http://localhost:8086'
token = 'DugaItJRzzLbbNgUrEuoWxv84iIE8LS68eNUhuXgRKrzabA62vIBfqn9H2LhIyACArjqEKG1t7b2CXY5gyDP7A=='
org = 'Data'
bucket = 'Csv'
kafka_bootstrap_servers = ['localhost:9092']
kafka_topic = 'sensor_data'

read_csv_and_write_to_influxdb_and_kafka(csv_file_path, influxdb_url, token, org, bucket, kafka_bootstrap_servers, kafka_topic)
