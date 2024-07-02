from confluent_kafka import Producer


def create_producer(config):
    return Producer(config)
