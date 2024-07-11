# pre_process.py
from confluent_kafka import KafkaError
from scipy import signal
import json

# Global lists to store raw and filtered records
raw_records = []
filtered_records = []


def iir_filter(input_value, b, a, zi):
    """
    IIR滤波器

    参数:
    input_value - 输入值
    b, a - 滤波器系数
    zi - 初始状态

    返回:
    output_value - 经过滤波后的输出值
    zi - 更新后的状态
    """
    output_value, zi = signal.lfilter(b, a, [input_value], zi=zi)
    return output_value[0], zi


def fetch_data(consumer):
    b, a = signal.butter(4, 0.3)  # 4th order Butterworth filter, cutoff frequency 0.3
    zi = signal.lfilter_zi(b, a) * 0  # Initialize filter state
    records = []
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        record = json.loads(msg.value().decode('utf-8'))
        value = record.get('Value', None)
        if value is not None:
            if isinstance(value, list) and len(value) > 0:
                for v in value:
                    filtered_value, zi = iir_filter(v, b, a, zi)
                    raw_records.append(v)
                    filtered_records.append(filtered_value)
            else:
                filtered_value, zi = iir_filter(value, b, a, zi)
                raw_records.append(value)
                filtered_records.append(filtered_value)
        records.append(record)
    return records
