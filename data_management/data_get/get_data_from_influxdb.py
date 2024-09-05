from influxdb_client import InfluxDBClient
from data_management.setting import settings


def data_get(year, exp_name, state, sensor_id):
    if state == "原始数据":
        state = 'ori'
        records = data_get_ori_and_pre(year, exp_name, state, sensor_id)
        return records
    elif state == "预处理数据":
        state = 'pre'
        records = data_get_ori_and_pre(year, exp_name, state, sensor_id)
        return records
    elif state == "特征提取":
        state = 'fix'
        records = data_get_fix(year, exp_name, state, sensor_id)
        return records


# 获取一次实验的原始数据
def data_get_ori_and_pre(year, exp_name, state, sensor_id):
    client = InfluxDBClient(**settings)
    query_api = client.query_api()
    measurement = year + '_' + exp_name + '_' + state
    query = """from(bucket: "test1")
        |> range(start: 0)
        |> filter(fn: (r) => r["_measurement"] == "{}")
        |> filter(fn: (r) => r["SensorID"] == "{}")
        |> filter(fn: (r) => r["_field"] == "Value" or r["_field"] == "Time" or r["_field"] == "Position")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        """.format(measurement, sensor_id)
    tables = query_api.query(query)
    datas = []
    for table in tables:
        for row in table:
            time_value_pair = [row['Time'], row['Value']]
            datas.append(time_value_pair)
    records = {
        'SensorId': sensor_id,
        'data': datas
    }
    return records
    # records = {'Acceleration': [], 'Strain': [], 'Temperature': [], 'Pressure': []}
    # for table in tables:
    #     for record in table:
    #         sensor_id = record['SensorID']
    #         sensor_type = record['Type']
    #         position = record['Position']
    #         time_value_pair = [record['Time'], record['Value']]
    #         sensor_data_entry = next((item for item in records[sensor_type] if item['SensorId'] == sensor_id), None)
    #         if not sensor_data_entry:
    #             sensor_data_entry = {
    #                 'SensorId': sensor_id,
    #                 'Type': sensor_type,
    #                 'Position': position,
    #                 'X-axis-name': 'Time',
    #                 'Y-axis-name': 'Value',
    #                 'data': []
    #             }
    #             records[sensor_type].append(sensor_data_entry)
    #         sensor_data_entry['data'].append(time_value_pair)
    # return records


def data_get_fix(year, exp_name, state, sensor_id):
    client = InfluxDBClient(**settings)
    query_api = client.query_api()
    measurement = year + '_' + exp_name + '_' + state
    query = """from(bucket: "test1")
            |> range(start: 0)
            |> filter(fn: (r) => r["_measurement"] == "{}")
            |> filter(fn: (r) => r["SensorID"] == "{}")
            |> filter(fn: (r) => r["_field"] == "Mean" or r["_field"] == "Max" or r["_field"] == "Min" or
            r["_field"] == "StdDev" or r["_field"] == "PeakToPeak") 
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            """.format(measurement, sensor_id)
    tables = query_api.query(query)
    data = {}
    for table in tables:
        for row in table:
            data = {
                'SensorId': sensor_id,
                'Max': row['Max'],
                'Min': row['Min'],
                'Mean': row['Mean'],
                'StdDev': row['StdDev'],
                'PeakToPeak': row['PeakToPeak'],
            }
    return data
    # records = {'Acceleration': [], 'Strain': [], 'Temperature': [], 'Pressure': []}
    # for table in tables:
    #     for record in table:
    #         sensor_id = record['SensorID']
    #         sensor_type = record['Type']
    #         cur_fixture = {
    #             'SensorId': sensor_id,
    #             'Mean': record['Mean'],
    #             'Max': record['Max'],
    #             'Min': record['Min'],
    #             'StdDev': record['StdDev'],
    #             'PeakToPeak': record['PeakToPeak'],
    #         }
    #         records[sensor_type].append(cur_fixture)
    # return records

