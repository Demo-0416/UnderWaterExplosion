import pandas as pd
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

from data_management.models import History
from data_management.setting import settings
from data_management.setting import csv_file_path
from data_management import models


class DataSaver:

    def read_csv_and_write_to_influxdb(self, year, exp_name):
        client = InfluxDBClient(**settings)
        write_api = client.write_api(write_options=WriteOptions(batch_size=1000))
        measurement = year + '_' + exp_name + '_ori'
        cur_csv_file_path = csv_file_path + year + "_" + exp_name + '_sensor_data.csv'
        # 读取 CSV 文件并将数据写入 InfluxDB
        df = pd.read_csv(cur_csv_file_path)
        points = []
        for index, row in df.iterrows():
            point = Point(measurement)  # 替换为你的测量名称
            point = point.tag("SensorID", row['SensorID'])  # 添加 SensorID 作为标签
            point = point.tag("Type", row['Type'])
            point = point.field("Position", row['Position'])
            point = point.field("Value", row['Value'])
            point = point.field("Time", row['Time'])  # 添加时间戳
            points.append(point)

        try:
            write_api.write(bucket=settings['bucket'], org=settings['org'], record=points)
            client.close()
            msg = FollowExp().create_history(year, exp_name)
            print('Successfully wrote ori_data to InfluxDB')
            return msg
        except Exception as e:
            print(e)



    # 将预处理后数据存入influxdb
    def save_pre_to_db(self, year, exp_name, records):
        # 更改records格式
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
        client = InfluxDBClient(**settings)
        write_api = client.write_api(write_options=WriteOptions(batch_size=1000))
        measurement = year + '_' + exp_name + '_pre'
        points = []
        for record in all_records:
            point = Point(measurement)  # 替换为你的测量名称
            point = point.tag("SensorID", record['SensorID'])  # 添加 SensorID 作为标签
            point = point.tag("Type", record['Type'])
            point = point.field("Position", record['Position'])
            point = point.field("Value", record['Value'])
            point = point.field("Time", record['Time'])
            points.append(point)

        try:
            write_api.write(bucket=settings['bucket'], org=settings['org'], record=points)
            client.close()
            print('Successfully wrote pre_data to InfluxDB')
        except Exception as e:
            print(e)


    def save_fix_to_db(self, year, exp_name, features):
        try:
            client = InfluxDBClient(**settings)
            write_api = client.write_api(write_options=SYNCHRONOUS)
            measurement = year + '_' + exp_name + '_fix'
            points = []
            for key, records in features.items():
                for record in records:
                    point = Point(measurement)
                    point = point.tag("Type", key)
                    point = point.tag("SensorID", record['SensorID'])
                    point = point.field("Mean", record['Mean'])
                    point = point.field("Max", record['Max'])
                    point = point.field("Min", record['Min'])
                    point = point.field("StdDev", record['StdDev'])
                    point = point.field("PeakToPeak", record['PeakToPeak'])
                    points.append(point)

            write_api.write(bucket=settings['bucket'], org=settings['org'], record=points)
            print('Successfully wrote fix_data to InfluxDB')
            client.close()
        except Exception as e:
            print(e)






# 生成或修改history内容用于跟踪每一次实验的状态
class FollowExp:

    def print_all_history(self):
        try:
            # 查询 History 模型的所有记录
            all_records = models.History.objects.all()
            
            # 如果有数据，逐条打印
            if all_records:
                for record in all_records:
                    print(f"Year: {record.save_time}, Experiment Name: {record.exp_name}, Status: {record.status}")
            else:
                print("数据库中没有记录。")
        except Exception as e:
            print(f"发生错误: {str(e)}")


    # 新增一次实验记录
    def create_history(self, year, exp_name,status):
        try:
            new_history = models.History(save_time=year, exp_name=exp_name, status=status)
            new_history.save()
            msg = "新实验生成成功"
            return msg
        except Exception as e:
            return str(e)

    # 修改一次实验的状态从“原始数据”到“预处理后数据”
    def change_state_to_pre(self, year, exp_name):
        try:
            count = History.objects.filter(save_time=year, exp_name=exp_name).update(status='pre')
            if count == 0:
                msg = "更新状态失败，未查询到该实验记录"
                print(msg)
                return msg
            elif count == 1:
                msg = "更新成功"
                print(msg)
                return msg
            else:
                msg = "发生错误，存在多项同名实验记录"
                print(msg)
                return msg
        except Exception as e:
            return str(e)

    # 修改一次实验的状态从“预处理后数据”到“特征提取”
    def change_state_to_fix(self, year, exp_name):
        try:
            count = History.objects.filter(save_time=year, exp_name=exp_name).update(status='特征提取')
            if count == 0:
                msg = "更新状态失败，未查询到该实验记录"
                return msg
            elif count == 1:
                msg = "更新成功"
                return msg
            else:
                msg = "发生错误，存在多项同名实验记录"
                return msg
        except Exception as e:
            return str(e)

    # 删除一次实验记录
    def delete_history(self, year, exp_name):
        try:
            count = History.objects.filter(save_time=year, exp_name=exp_name).delete()
            if count == 0:
                msg = "删除失败，未查询到该实验记录"
                return msg
            elif count == 1:
                msg = "删除成功"
                return msg
            else:
                msg = "发生错误，存在多项同名实验记录"
                return msg
        except Exception as e:
            return str(e)





