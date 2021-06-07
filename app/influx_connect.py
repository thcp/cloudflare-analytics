#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from influxdb import InfluxDBClient
from config_loader import get_config

host = get_config('INFLUXDB', 'host')
port = get_config('INFLUXDB', 'port')
port = get_config('INFLUXDB', 'port')
username = get_config('INFLUXDB', 'username')
database = get_config('INFLUXDB', 'database')
password = os.environ.get('INFLUXDB_PASSWORD')

def influxdb_publish(data):
    client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)
    try:
        client.write_points(data)
    except:
        raise
