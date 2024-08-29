import threading
from django.http import HttpResponse, JsonResponse
from scipy import signal
from confluent_kafka import Consumer, KafkaException
import json
from data_processing.preprocess.pre_algorithem import fetch_data,generate_plots
from data_processing.feature.feature_extraction import extract_features
from django.core.cache import cache

# Global lists to store raw and filtered records
raw_records = []
filtered_records = []
lock = threading.Lock()


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
        lock_acquired = lock.acquire(blocking=False)
        if not lock_acquired:
            print("Lock not acquired, data fetching is in progress.")
            return JsonResponse({
                'status': 'info',
                'message': '数据获取正在进行，请稍等。'
            }, status=200)

        try:
            print("Lock acquired, starting consumer setup...")
            consumer = Consumer({
                'bootstrap.servers': 'localhost:9092',
                'group.id': 'sensor_data_group',
                'auto.offset.reset': 'earliest',
                'enable.auto.commit': False
            })

            kafka_topics = [f'location_{i}_data_topic' for i in range(1, 26)]
            print(f"Subscribing to topics: {kafka_topics}")

            consumer.subscribe(kafka_topics)

            print("Fetching data from Kafka...")
            records = fetch_data(consumer)
            cache.set('preprocessed_data', records, timeout=3600)
            print("Data fetched successfully.")

            consumer.commit()

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

        finally:
            print("Releasing lock and closing consumer.")
            consumer.close()
            lock.release()

    else:
        return JsonResponse({
            'status': 'error',
            'message': '不允许的请求方法。只支持 GET 请求。'
        }, status=405)

def extract_features_view(request):
    if request.method == 'GET':
        try:
            # consumer = Consumer({
            #     'bootstrap.servers': 'localhost:9092',
            #     'group.id': 'sensor_data_group',
            #     'auto.offset.reset': 'earliest'
            # })
            # kafka_topics = [f'location_{i}_data_topic' for i in range(1, 26)]
            # consumer.subscribe(kafka_topics)

            # records = fetch_data(consumer)
            # features = extract_features(records)
            preprocessed_data = cache.get('preprocessed_data')
            if not preprocessed_data:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No preprocessed data available. Please preprocess the data first.'
                }, status=404)

            # 进行特征提取
            features = extract_features(preprocessed_data)

            cache.delete('preprocessed_data')

            return JsonResponse({
                'status': 'success',
                'features': features
            }, status=200, safe=False)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed. Only GET requests are supported.'
        }, status=405)