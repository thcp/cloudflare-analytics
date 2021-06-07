#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import influx_connect

def template():
    return [
        {
            "tags": {
                "zone": ""
            },
            "time": "",
            "fields": {
            }
        }
    ]

def parse_graphql_data(zone_name, data):
    log_date = data["dimensions"]["datetimeMinute"]
    browser_map = []
    country_map = []
    response_status_map = []
    threat_pathing_map = []
    content_type_map = []
    sum_map = []
    
    print(json.dumps(data, indent=4, sort_keys=True))
    for (key, value) in data.items():
        for (k, v) in value.items():
            if isinstance(v, (dict, list, tuple,)):
                for vv in v:
                    if k == 'browserMap':
                        browser_map.append(vv)
                    elif k == 'countryMap':
                        country_map.append(vv)
                    elif k == 'responseStatusMap':
                        response_status_map.append(vv)
                    elif k == 'threatPathingMap':
                        threat_pathing_map.append(vv)
                    elif k == 'contentTypeMap':
                        content_type_map.append(vv)
            else:
                d = {
                    k: v
                }
                sum_map.append(d)
                
    if browser_map:
        browser_map_template(zone_name, log_date, browser_map)
    if sum_map:
        sum_map_template(zone_name, log_date, sum_map)
    if country_map:
        country_map_template(zone_name, log_date, country_map)
    if response_status_map:
        response_status_map_template(zone_name, log_date, response_status_map)
    if threat_pathing_map:
        threat_pathing_map_template(zone_name, log_date, threat_pathing_map)
    if content_type_map:
        content_type_map_template(zone_name, log_date, content_type_map)
    

def country_map_template(zone_name, parse_date, data):
    t = template()
    t[0]['measurement'] = "analytics_country_map"
    t[0]['tags']['zone'] = zone_name
    t[0]['time'] = parse_date
    for d in data:
        for (key, value) in d.items():
            if key == 'clientCountryName':
                t[0]['tags'][key] = value
            t[0]['fields'][key] = value
    influx_connect.influxdb_publish(t)

def browser_map_template(zone_name, parse_date, data):
        t = template()
        t[0]['measurement'] = "analytics_browser_map"
        t[0]['tags']['zone'] = zone_name
        t[0]['time'] = parse_date
        for d in data:
            for (key, value) in d.items():
                if key == 'uaBrowserFamily':
                    t[0]['tags'][key] = value
                if key:
                    t[0]['fields'][key] = value
        influx_connect.influxdb_publish(t)

def response_status_map_template(zone_name, parse_date, data):
    t = template()
    t[0]['measurement'] = "analytics_response_status_map"
    t[0]['tags']['zone'] = zone_name
    t[0]['time'] = parse_date
    for d in data:
        for (key, value) in d.items():
            if key == 'edgeResponseStatus':
                t[0]['tags'][key] = value
            if key:
                t[0]['fields'][key] = value
    influx_connect.influxdb_publish(t)


def threat_pathing_map_template(zone_name, log_date, data):
    #Value isnt in use yet
    pass

def content_type_map_template(zone_name, parse_date, data):
    t = template()
    t[0]['measurement'] = "analytics_response_content_type_map"
    t[0]['tags']['zone'] = zone_name
    t[0]['time'] = parse_date
    for d in data:
        for (key, value) in d.items():
           t[0]['fields'][key] = value
    influx_connect.influxdb_publish(t)

def sum_map_template(zone_name, parse_date, data):
    t = template()
    t[0]['measurement'] = "analytics_response_sum_map"
    t[0]['tags']['zone'] = zone_name
    t[0]['time'] = parse_date
    for d in data:
        for (key, value) in d.items():
           t[0]['fields'][key] = value
    influx_connect.influxdb_publish(t)