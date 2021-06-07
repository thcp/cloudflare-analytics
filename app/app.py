#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import datetime
import cloudflare
from config_loader import get_config

cf_fetch_interval = get_config('APP', 'fetch_interval')


def fetch_analytics_by_zone():
    for zone in cloudflare.get_zone_details():
        zone_name = zone['zone_name']
        zone_id = zone['zone_id']
        print("Retrieving: {}".format(zone_name))
        cloudflare.run_query(zone_id, zone_name)


if __name__ == '__main__':
    REQUIRED_VARS = {'CF_AUTH_EMAIL', 'CF_AUTH_KEY', 'CF_GLOBAL_KEY', 'INFLUXDB_PASSWORD'}
    for key in REQUIRED_VARS:
        if key not in os.environ:
            print('Environment var not set for {}'.format(key))
    
    while True:
        fetch_analytics_by_zone()
        print('Sleeping for {} seconds'.format(cf_fetch_interval))
        time.sleep(cf_fetch_interval)
