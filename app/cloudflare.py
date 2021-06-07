#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json
import datetime
import pytz
import CloudFlare
import requests
from config_loader import get_config
import influx_template_builder

cf_freeplans = get_config('CLOUDFLARE', 'bypass_domains')
cf_api_url = get_config('CLOUDFLARE', 'api_url')
cf_page_limit = get_config('CLOUDFLARE', 'page_limit')

auth_email = os.environ.get('CF_AUTH_EMAIL')
user_token = os.environ.get('CF_AUTH_KEY')
cf_token = os.environ.get('CF_GLOBAL_KEY')


def now_iso8601_time(h_delta):
    t = time.time() - h_delta
    r = datetime.datetime.fromtimestamp(int(t), tz=pytz.timezone("UTC")).strftime('%Y-%m-%dT%H:%M:%SZ')
    return r


def get_zone_details():
    zone_info = []
    cf = CloudFlare.CloudFlare(token=user_token)
    zones = cf.zones.get(params={'per_page': cf_page_limit})
    for zone in zones:
        zone_data = {
            'zone_name': zone['name'],
            'zone_id': zone['id']
        }
        if zone['name'] in cf_freeplans:
            pass
        else:
            zone_info.append(zone_data)
    return zone_info


def run_query(zone_id, zone_name):
    date_after = now_iso8601_time(600)
    cf = CloudFlare.CloudFlare(token=cf_token, email=auth_email)
    query = http_requests_by_minute(zone_id, date_after)
    try:
        r = cf.graphql.post(data={'query': query})
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/graphql.post %d %s - api call failed' % (e, e))
    else:
        zone_info = r['data']['viewer']['zones'][0]
        http_requests = zone_info['httpRequests1mGroups']
        for h in http_requests:
          influx_template_builder.parse_graphql_data(zone_name, h)


def http_requests_by_minute(zone_id, date_after):
    query = """
    {
      viewer {
        zones(filter: {zoneTag: "%s"}) {
          httpRequests1mGroups(orderBy: [datetimeMinute_ASC], limit: 100, filter: {datetime_gt: "%s"}) {
            dimensions {
              datetimeMinute
            }
            sum {
              browserMap {
                pageViews
                uaBrowserFamily
              }
              bytes
              cachedBytes
              cachedRequests
              contentTypeMap {
                bytes
                requests
                edgeResponseContentTypeName
              }              
              countryMap {
                bytes
                requests
                threats
                clientCountryName
              }
              pageViews
              requests
              responseStatusMap {
                requests
                edgeResponseStatus
              }
              threats
              threatPathingMap {
                requests
                threatPathingName
              }
            }
            uniq {
              uniques
            }
          }
        }
      }
    }     
    """ % (zone_id, date_after)
    return query
