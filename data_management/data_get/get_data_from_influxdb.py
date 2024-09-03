from influxdb_client import InfluxDBClient
from data_management.setting import settings


# 获取一次实验的原始数据
def data_get(year, exp_name, state):
    client = InfluxDBClient(**settings)
    if state == "原始数据":
        state = 'ori'
    if state == "预处理数据":
        state = 'pre'
    if state == "特征提取":
        state = 'fix'
    query_api = client.query_api()
    measurement = year + '_' + exp_name + '_' + state
    print(measurement)
    query = """from(bucket: "test1")
        |> range(start: 0)
        |> filter(fn: (r) => r["_measurement"] == "{}")
        |> filter(fn: (r) => r["_field"] == "Value" or r["_field"] == "Time" or r["_field"] == "Position")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        """.format(measurement)
    tables = query_api.query(query)
    records = {'Acceleration': [], 'Strain': [], 'Temperature': [], 'Pressure': []}
    for table in tables:
        for record in table:
            sensor_id = record['SensorID']
            sensor_type = record['Type']
            position = record['Position']
            time_value_pair = [record['Time'], record['Value']]
            sensor_data_entry = next((item for item in records[sensor_type] if item['SensorID'] == sensor_id), None)
            if not sensor_data_entry:
                sensor_data_entry = {
                    'SensorID': sensor_id,
                    'Type': sensor_type,
                    'Position': position,
                    'X-axis-name': 'Time',
                    'Y-axis-name': 'Value',
                    'data': []
                }
                records[sensor_type].append(sensor_data_entry)
            sensor_data_entry['data'].append(time_value_pair)
    return records
