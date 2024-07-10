import threading
import matplotlib.pyplot as plt
import io
import base64
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from confluent_kafka import Consumer, KafkaError
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

def consume_sensor_data(request):
    if request.method == 'GET':
        records = []
        global raw_records, filtered_records
        raw_records = []
        filtered_records = []
        consumer = Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'sensor_data_group',
            'auto.offset.reset': 'earliest'
        })
        consumer.subscribe(['temperature_data_topic'])

        def fetch_data():
            b, a = signal.butter(4, 0.3)  # 4th order Butterworth filter, cutoff frequency 0.3
            zi = signal.lfilter_zi(b, a) * 0  # Initialize filter state
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

        threading.Thread(target=fetch_data).start()
        return JsonResponse({'status': 'consuming started'})

def plot_filtered_data(request):
    if request.method == 'GET':
        global raw_records, filtered_records
        if not raw_records or not filtered_records:
            return HttpResponse("No data to plot")

        # Create a time array
        time_interval = 0.01
        min_length = min(len(raw_records), len(filtered_records))
        time_array = [i * time_interval for i in range(min_length)]
        
        raw_records = raw_records[:min_length]
        filtered_records = filtered_records[:min_length]

        plt.figure(figsize=(10, 6))
        plt.plot(time_array, raw_records, label='Raw Data', alpha=0.7)
        plt.plot(time_array, filtered_records, label='Filtered Data', alpha=0.7)
        plt.xlabel('Time (s)')
        plt.ylabel('Value')
        plt.title('Raw and Filtered Sensor Data')
        plt.legend()

        # Save plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        # Encode the plot in base64 to send as a response
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return HttpResponse(f'<img src="data:image/png;base64,{image_base64}" />')

# URL configuration should include this view
