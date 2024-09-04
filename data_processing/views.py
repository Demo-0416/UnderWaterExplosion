import threading
from django.http import JsonResponse
import pandas as pd
from scipy import signal
from confluent_kafka import Consumer, KafkaException
import json
from data_processing.preprocess.pre_algorithem import fetch_data
from data_processing.feature.feature_extraction import extract_features
from django.core.cache import cache
from data_management.data_input.file_uploader import FollowExp
from data_management.data_input.file_uploader import  DataSaver
from django.views.decorators.csrf import csrf_exempt

# Global lists to store raw and filtered records
raw_records = []
filtered_records = []
lock = threading.Lock()  # 用于consume_sensor_data的锁
feature_lock = threading.Lock()  # 用于extract_features_view的锁

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

@csrf_exempt
def consume_sensor_data(request):
    if request.method == 'POST':
        lock_acquired = lock.acquire(blocking=False)
        if not lock_acquired:
            print("Lock not acquired, data fetching is in progress.")
            return JsonResponse({
                'status': 'info',
                'message': '数据获取正在进行，请稍等。'
            }, status=200)

        try:
            print("Lock acquired, starting consumer setup...")

            # 从请求体中获取年份和实验名
            data = json.loads(request.body)
            year = data.get('Year')
            exp_name = data.get('Exp_name')

            if not year or not exp_name:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Year and experiment name are required.'
                }, status=400)

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

            # 保存数据到db
            DataSaver().save_pre_to_db(year, exp_name, records)

            # 保存数据到 CSV 文件
            # filename = f"{year}_{exp_name}_preprocess_data.csv"
            # save_records_to_csv(records, filename)

            # 改变该实验标识的status
            FollowExp().change_state_to_pre(year=year, exp_name=exp_name)

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
            'message': '不允许的请求方法。只支持 POST 请求。'
        }, status=405)


def save_records_to_csv(records, filename):
    # 将处理后的记录保存为CSV文件
    all_records = []
    for sensor_type, sensor_data in records.items():
        for data_entry in sensor_data:
            sensor_id = data_entry['SensorID']
            sensor_type = data_entry['Type']
            position = data_entry['Position']
            for data_point in data_entry['data']:
                all_records.append({
                    'Time': data_point['Time'],
                    'SensorID': sensor_id,
                    'Type': sensor_type,
                    'Position': position,
                    'Value': data_point['Value']
                })

    # 将记录转换为DataFrame并保存为CSV
    df = pd.DataFrame(all_records)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

@csrf_exempt
def extract_features_view(request):
    if request.method == 'POST':
        feature_lock_acquired = feature_lock.acquire(blocking=False)
        if not feature_lock_acquired:
            print("Lock not acquired, feature extraction is in progress.")
            return JsonResponse({
                'status': 'info',
                'message': '特征提取正在进行，请稍等。'
            }, status=200)

        try:
            data = json.loads(request.body)
            year = data.get('Year')
            exp_name = data.get('Exp_name')
            preprocessed_data = cache.get('preprocessed_data')
            if not preprocessed_data:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No preprocessed data available. Please preprocess the data first.'
                }, status=404)

            # 进行特征提取
            features = extract_features(preprocessed_data)
            print("start save fixture to db")
            DataSaver().save_fix_to_db(year, exp_name, features)
            print("finish save fixture to db")
            FollowExp().change_state_to_fix(year=year, exp_name=exp_name)
            print("标记重新设置")
            
            # # 将特征保存到 CSV 文件
            # year = '2024'  # 示例年份，实际应用中从请求中获取年份
            # exp_name = 'features'  # 示例实验名称，实际应用中从请求中获取实验名称
            # filename = f'{year}_{exp_name}_features.csv'
            # df = pd.DataFrame(features)
            # df.to_csv(filename, index=False)
            # print(f"Features saved to {filename}")

            # 从缓存中删除预处理数据
            cache.delete('preprocessed_data')

            return JsonResponse({
                'status': 'success',
                'message': f'Features extracted and saved'
            }, status=200)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

        finally:
            print("Releasing feature extraction lock.")
            feature_lock.release()

    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed. Only POST requests are supported.'
        }, status=405)