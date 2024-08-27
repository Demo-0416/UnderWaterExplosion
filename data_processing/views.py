import threading
from django.http import HttpResponse, JsonResponse
from scipy import signal
from confluent_kafka import Consumer, KafkaException
import json
from data_processing.preprocess.pre_algorithem import fetch_data,generate_plots

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
        try:
            print("Starting consumer setup...")
            consumer = Consumer({
                'bootstrap.servers': 'localhost:9092',
                'group.id': 'sensor_data_group',
                'auto.offset.reset': 'earliest'
            })

            kafka_topics = [f'location_{i}_data_topic' for i in range(1, 26)]
            print(f"Subscribing to topics: {kafka_topics}")

            consumer.subscribe(kafka_topics)

            print("Fetching data from Kafka...")
            records = fetch_data(consumer)
            print("Data fetched successfully.")
            
            return JsonResponse({
                'status': 'success',
                'data': records
            }, status=200, safe=False)

        except KafkaException as e:
            print(f"Kafka error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"Kafka error: {str(e)}"
            }, status=500)
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"JSON decode error: {str(e)}"
            }, status=400)

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"Unexpected error: {str(e)}"
            }, status=500)

    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed. Only GET requests are supported.'
        }, status=405)
        # print("Generating plots...")
        # plot_html = generate_plots(records)
        # print("Plots generated successfully.")
        
        # return HttpResponse(plot_html)




