from confluent_kafka import Producer, KafkaError
import csv
import time

# Kafka 服务器地址
bootstrap_servers = 'localhost:9092'

# Kafka 主题名称
topic = 'test-topic'

def delivery_report(err, msg):
    """ Kafka 生产者消息发送回调函数 """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def produce_from_csv(csv_file):
    """ 从 CSV 文件生成 Kafka 生产者流 """
    producer = Producer({'bootstrap.servers': bootstrap_servers})

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # 将 CSV 行数据转换为 Kafka 消息格式
            message = f"{row['Time']},{row['SensorID']},{row['Type']},{row['Position']},{row['Value']}"
            producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
            time.sleep(0.1)  # 可选：控制消息发送速率

    producer.flush()  # 确保所有消息都已发送

if __name__ == '__main__':
    csv_file_path = 'E:/PythonMyTest/test_data.csv'  # 替换为你的 CSV 文件路径
    produce_from_csv(csv_file_path)
