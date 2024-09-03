from django.http import JsonResponse
from django.shortcuts import render
import numpy as np
import threading
from .data_input.data_simulator import DataSimulator
from .data_input.file_uploader import DataSaver
from influxdb.exceptions import InfluxDBClientError
import json
from .data_get.get_data_from_influxdb import ori_data_get

from django.views.decorators.http import require_http_methods

from .models import History

# 参数配置
params_simulator = {
    'P0': 1000, 'alpha': 0.1, 'nu': 0.05, 'omega': 2 * np.pi * 10, 'beta': 1,
    'T0': 20, 'DeltaT': 5, 'gamma': 0.05, 'phi': 2 * np.pi * 0.5, 'delta': 0.5,
    'epsilon0': 0.001, 'kappa': 0.1, 'psi': 2 * np.pi * 1, 'eta': 0.2
}

# 初始化模拟器
simulator = DataSimulator(params_simulator)
data_saver = DataSaver()

stream_lock = threading.Lock()
# 用于指示数据流线程是否正在运行
is_streaming = False  

def stream_sensor_data(request):
    global is_streaming

    if request.method == 'GET':
        # 尝试获取锁
        if not stream_lock.acquire(blocking=False):  # 如果锁不可用，则返回错误信息
            return JsonResponse({
                'status': 'error',
                'message': 'Streaming is already in progress. Please wait until the current stream is finished.'
            }, status=423)  # 423 Locked 状态码表示资源被锁定
        
        try:
            # 检查是否已经在流数据
            if is_streaming:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Streaming is already in progress. Please wait until the current stream is finished.'
                }, status=423)

            # 设置为流数据状态
            is_streaming = True

            positions = np.linspace(100, 1000, 25)  # 生成 25 个位置，每个位置的值是整数
            kafka_topics = [f'location_{i}_data_topic' for i in range(1, 26)]
            explosion_duration = 1  # 每次爆炸持续时间
            num_explosions = 5  # 爆炸次数

            # 启动数据流线程
            threading.Thread(target=stream_data_with_lock, args=(positions, explosion_duration, kafka_topics, num_explosions)).start()

            return JsonResponse({'status': 'streaming started'}, status=200)

        except Exception as e:
            # 释放锁并重置状态
            is_streaming = False
            stream_lock.release()

            return JsonResponse({
                'status': 'error',
                'message': f"Unexpected error: {str(e)}"
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed. Only GET requests are supported.'
    }, status=405)

def stream_data_with_lock(positions, explosion_duration, kafka_topics, num_explosions):
    global is_streaming
    try:
        simulator.stream_sensor_data(positions, explosion_duration, kafka_topics, num_explosions)
    finally:
        # 确保流数据线程结束时释放锁和重置状态
        is_streaming = False
        stream_lock.release()

def save_sensor_data(request):
    if request.method == 'GET':
        try:
            year = request.GET['Year']
            exp_name = request.GET['Exp_Name']
            positions = np.linspace(100, 1000, 25)  # 生成 25 个位置，每个位置的值是整数
            duration = 1  # 持续时间 1 秒
            filename = year + exp_name + "sensor_data.csv"
            num_explosions = 5  # 爆炸次数

            # 调用 save_sensor_data 方法保存数据到 CSV 文件
            simulator.save_sensor_data(positions, duration, filename, num_explosions)

            return JsonResponse({'status': 'save completed'}, status=200)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f"Unexpected error: {str(e)}"
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed. Only GET requests are supported.'
    }, status=405)


def save_to_db(request):
    if request.method == 'GET':
        try:
            year = request.GET['Year']
            exp_name = request.GET['Exp_Name']
            if year is None:
                return JsonResponse({'status': 'error', 'message': 'Year is required'}, status=400)
            if exp_name is None:
                return JsonResponse({'status': 'error', 'message': 'Exp_Name is required'}, status=400)
            # 调用方法将数据保存到 InfluxDB
            data_saver.read_csv_and_write_to_influxdb(year, exp_name)

            return JsonResponse({'status': 'save to database'}, status=200)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f"Unexpected error: {str(e)}"
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed. Only GET requests are supported.'
    }, status=405)


# 获取一次实验的全部数据
def get_ori_data(request):
    if request.method == "GET":
        try:
            year = request.GET["Year"]
            exp_name = request.GET["Exp_Name"]
            
            if year is None:
                return JsonResponse({'code': '4', 'message': 'Year 参数缺失或无效。'})
            if exp_name is None:
                return JsonResponse({'code': '4', 'message': 'Exp_Name 参数缺失或无效。'})
            data = ori_data_get(year, exp_name)
            return JsonResponse({'code': '0', 'data': data})
        except InfluxDBClientError as e:
            print(f"InfluxDBClient error: {str(e)}")
            return JsonResponse({
                'code': '1',
                'message': f"Unexpected error: {str(e)}"
            })
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {str(e)}")
            return JsonResponse({
                'code': '6',
                'message': f"JSONDecodeError: {str(e)}"
            })
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({
                'code': '2',
                'message': f"Unexpected error: {str(e)}"
            })
    else:
        return JsonResponse({'code': '3', 'message': '不允许的请求方法。只支持 GET 请求。'})
    
@require_http_methods(["GET"])
def get_test_data(request):
        try:
            # request_body = json.loads(request.body)
            # year = request_body['Year']
            # exp_name = request_body['Exp_Name']
            year = request.GET["Year"]
            exp_name = request.GET["Exp_Name"]
            
            if year is None:
                return JsonResponse({'code': '4', 'message': 'Year 参数缺失或无效。'})
            if exp_name is None:
                return JsonResponse({'code': '4', 'message': 'Exp_Name 参数缺失或无效。'})
            return JsonResponse({'code': '0', 'data': 'test'})
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({
                'code': '2',
                'message': f"Unexpected error: {str(e)}"
            })


# 返回历史实验的标记
def get_history(request):
    if request.method == "GET":
        try:
            history_list = History.objects.all()
            print(history_list)
            json_list = json.loads(json.dumps([{
                'year': item.save_time,
                'exp_name': item.exp_name,
            } for item in history_list]))

            return JsonResponse({'code': '0', 'data': json_list})
        except Exception as e:
            return JsonResponse({'code': '1', 'message': str(e)})
