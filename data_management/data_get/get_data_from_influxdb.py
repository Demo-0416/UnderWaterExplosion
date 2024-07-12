from influxdb_client import InfluxDBClient


# 参数待填
token = ""
org = ""
url = "http://localhost:8086"
bucket = ''
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()


# bucket代填
def select_single_sensor_data(SensorID, measurement, start_time):
    query_value = """from(bucket: "")
    |> range(start: {})
    |> filter(fn: (r) => r["_measurement"] == "{}")
    |> filter(fn: (r) => r["SensorID"] == "{}")
    |> filter(fn: (r) => r["_field"] == "Value" or r["_field"] == "Time" or r["_field"] == "Position")
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    """.format(start_time, measurement, SensorID)
    tables = query_api.query(query_value)
    member_list = []
    for table in tables:
        for record in table:
            member = {
                "measurement": measurement,
                "SensorID": SensorID,
                "position": record['Position'],
                "time": record['Time'],
                "value": record['Value']
            }
            member_list.append(member)
    return member_list


# 获取同一类型的数据
def select_type_data(measurement, start_time):
    query = """from(bucket: "")
    |> range(start: {})
    |> filter(fn: (r) => r["_measurement"] == "{}")
    |> filter(fn: (r) => r["_field"] == "Value" or r["_field"] == "Time" or r["_field"] == "Position")
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    """.format(start_time, measurement)
    tables = query_api.query(query)
    member_list = []
    for table in tables:
        for record in table:
            member = {
                "measurement": measurement,
                "SensorID": record['SensorID'],
                "position": record['Position'],
                "time": record['Time'],
                "value": record['Value']
            }
            member_list.append(member)
    return member_list


# 获取所有数据
def select_all_data(start_time):
    measurement_list = []
    all_data_list = []
    for measurement in measurement_list:
        member_list = select_type_data(measurement, start_time)
        all_data_list.extend(member_list)
    return all_data_list
