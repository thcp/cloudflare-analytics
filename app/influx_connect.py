from influxdb import InfluxDBClient
from config_loader import get_config

host = get_config('INFLUXDB', 'host')
port = get_config('INFLUXDB', 'port')
username = get_config('INFLUXDB', 'username')
password = get_config('INFLUXDB', 'password')
database = get_config('INFLUXDB', 'database')


def influxdb_publish(json_data):
    client = InfluxDBClient(host=host, port=port, username=username,
                            password=password, database=database)

    client.write_points(json_data)
