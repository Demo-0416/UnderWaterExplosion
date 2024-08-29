# your_app_name/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from confluent_kafka import Consumer, KafkaException, KafkaError
from scipy import signal

class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket connection established.")

    async def disconnect(self, close_code):
        print("WebSocket connection closed.")

    async def receive(self, text_data):
        print(f"Received message: {text_data}")
        # 在接收到消息时，开始从 Kafka 读取数据并处理
        records = await self.fetch_data()
        await self.send(text_data=json.dumps(records))

    async def fetch_data(self):
        # Kafka 消费者设置
        consumer = Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'sensor_data_group',
            'auto.offset.reset': 'earliest'
        })

        kafka_topics = [f'location_{i}_data_topic' for i in range(1, 26)]
        consumer.subscribe(kafka_topics)

        # Butterworth 滤波器配置
        b, a = signal.butter(4, 0.3)  # 四阶 Butterworth 滤波器，截止频率为 0.3
        zi = signal.lfilter_zi(b, a) * 0  # 初始化滤波器状态

        records = {
            'Acceleration': [],
            'Strain': [],
            'Temperature': [],
            'Pressure': []
        }
        message_count = 0

        while message_count < 5:
            msg = consumer.poll(1.0)
            if msg is None:
                message_count += 1
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            record = json.loads(msg.value().decode('utf-8'))
            sensor_id = record.get('SensorID', None)  # 获取传感器 ID
            sensor_type = record.get('Type', None)    # 获取传感器类型
            value = record.get('Value', None)
            timestamp = record.get('Time', None)
            if value is not None and sensor_type in records:
                filtered_value, zi = signal.lfilter(b, a, [value], zi=zi)
                records[sensor_type].append({
                    'timestamp': timestamp,
                    'sensor_id': sensor_id,
                    'type': sensor_type,
                    'raw': value,
                    'filtered': filtered_value[0]
                })
                print(f"Fetched and processed record: {record}")

        consumer.close()
        return records
