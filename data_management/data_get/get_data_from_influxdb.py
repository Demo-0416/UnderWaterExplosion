from influxdb_client import InfluxDBClient


# 参数待填
token = ""
org = ""
url = "http://localhost:8086"
bucket = ''


# bucket代填
# def select_single_sensor_data(SensorID, measurement, start_time):
#     query_value = """from(bucket: "")
#     |> range(start: {})
#     |> filter(fn: (r) => r["_measurement"] == "{}")
#     |> filter(fn: (r) => r["SensorID"] == "{}")
#     |> filter(fn: (r) => r["_field"] == "Value" or r["_field"] == "Time" or r["_field"] == "Position")
#     |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
#     """.format(start_time, measurement, SensorID)
#     tables = query_api.query(query_value)
#     member_list = []
#     for table in tables:
#         for record in table:
#             member = {
#                 "measurement": measurement,
#                 "SensorID": SensorID,
#                 "position": record['Position'],
#                 "time": record['Time'],
#                 "value": record['Value']
#             }
#             member_list.append(member)
#     return member_list
#
#
# # 获取同一类型的数据
# def select_type_data(measurement, start_time):
#     query = """from(bucket: "")
#     |> range(start: {})
#     |> filter(fn: (r) => r["_measurement"] == "{}")
#     |> filter(fn: (r) => r["_field"] == "Value" or r["_field"] == "Time" or r["_field"] == "Position")
#     |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
#     """.format(start_time, measurement)
#     tables = query_api.query(query)
#     member_list = []
#     for table in tables:
#         for record in table:
#             member = {
#                 "measurement": measurement,
#                 "SensorID": record['SensorID'],
#                 "position": record['Position'],
#                 "time": record['Time'],
#                 "value": record['Value']
#             }
#             member_list.append(member)
#     return member_list
#
#
# # 获取所有数据
# def select_all_data(start_time):
#     measurement_list = []
#     all_data_list = []
#     for measurement in measurement_list:
#         member_list = select_type_data(measurement, start_time)
#         all_data_list.extend(member_list)
#     return all_data_list

settings = {
    'token': token,
    'org': org,
    'url': url,
    'bucket': bucket
}


def ori_data_get(year, exp_name):
    client = InfluxDBClient(**settings)
    query_api = client.query_api()
    measurement = year + '_' + exp_name + '_' + 'ori'
    query = """from(bucket: "test1")
        |> range(start: 0)
        |> filter(fn: (r) => r["_measurement"] == "{}")
        |> filter(fn: (r) => r["_field"] == "Value" or r["_field"] == "Time" or r["_field"] == "Position")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        """.format(measurement)
    tables = query_api.query(query)
    ori_record = {'Acceleration': [], 'Strain': [], 'Temperature': [], 'Pressure': []}
    for table in tables:
        for record in table:
            sensor_id = record['SensorID']
            sensor_type = record['Type']
            position = record['Position']
            time_value_pair = [record['Time'], record['Value']]
            sensor_data_entry = next((item for item in ori_record[sensor_type] if item['SensorID'] == sensor_id), None)
            if not sensor_data_entry:
                sensor_data_entry = {
                    'SensorID': sensor_id,
                    'Type': sensor_type,
                    'Position': position,
                    'X-axis-name': 'Time',
                    'Y-axis-name': 'Value',
                    'data': []
                }
                ori_record[sensor_type].append(sensor_data_entry)
            sensor_data_entry['data'].append(time_value_pair)
    return ori_record
