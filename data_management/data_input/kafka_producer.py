from confluent_kafka import Producer
import json


class KafkaProducer:
    def __init__(self, config):
        self.producer = Producer(config)

    def send(self, topic, data):
        self.producer.produce(topic, json.dumps(data).encode('utf-8'))
        self.producer.flush()
