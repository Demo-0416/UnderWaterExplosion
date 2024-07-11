from influxdb_client import InfluxDBClient


# 参数待填
token = ""
org = ""
url = "http://localhost:8086"
bucket = ''
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()


# bucket代填
def get_sensor_position(SensorID, measurement, start_time):
    query_position = """from(bucket: "")
    |> range(start: {})
    |> filter(fn: (r) => r["_measurement"] == "{}")
    |> filter(fn: (r) => r["SensorID"] == "{}")
    |> filter(fn: (r) => r["_field"] == "Position")
    |> distinct()
    |> yield(name: "distinct")
    """.format(start_time, measurement, SensorID)
    tables = query_api.query(query_position)
    for table in tables:
        for record in table:
            return record['_value']



# 通过传感器编号获取数据
def select_single_sensor_data(SensorID, measurement, start_time):
    query_value = """from(bucket: "")
    |> range(start: {})
    |> filter(fn: (r) => r["_measurement"] == "{}")
    |> filter(fn: (r) => r["SensorID"] == "{}")
    |> filter(fn: (r) => r["_field"] == "Value")
    """.format(start_time, measurement, SensorID)
    value_list = []
    value_tables = query_api.query(query_value)
    for table in value_tables:
        for record in table:
            value_list.append(record['_value'])
    query_time = """from(bucket: "")
    |> range(start: {})
    |> filter(fn: (r) => r["_measurement"] == "{}")
    |> filter(fn: (r) => r["SensorID"] == "{}")
    |> filter(fn: (r) => r["_field"] == "Time")
    """.format(start_time, measurement, SensorID)
    time_list = []
    time_tables = query_api.query(query_time)
    for table in time_tables:
        for record in table:
            time_list.append(record['_value'])
    member_list = []
    position = get_sensor_position(SensorID, measurement, start_time)
    for i in range(len(value_list)):
        member = {
            "measurement": measurement,
            "SensorID": SensorID,
            "position": position,
            "time": time_list[i],
            "value": value_list[i]
        }
        member_list.append(member)
    return member_list


# 获取同一类型的数据，如温度，加速度
def select_type_data(measurement, start_time):
    query = """from(bucket: "")
    |> range(start: {})
    |> filter(fn: (r) => r["_measurement"] == "{}")
    """.format(start_time, measurement)
    tables = query_api.query(query)


# 获取所有数据
def select_all_data(start_time):
    query = """from(bucket: "")
    |> range(start: {})
    """.format(start_time)
    talbes = query_api.query(query)