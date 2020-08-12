import CloudFlare
import json
import requests
from config_loader import get_config
import influx_json_templates as ijt
import time
import datetime

fetch_interval = int(get_config('APP', 'fetch_interval'))
cf_token = get_config('CLOUDFLARE', 'token')
cf_api_url = get_config('CLOUDFLARE', 'api_url')
cf_analytics_uri_prefix = get_config('CLOUDFLARE', 'analytics_uri_prefix')
cf_freeplans = get_config('CLOUDFLARE', 'free_plans')

def cf_zone_info():
    zone_info = []
    cf = CloudFlare.CloudFlare(token=cf_token)
    zones = cf.zones.get()
    for zone in zones:
        zone_data = {
            'zone_name': zone['name'],
            'zone_id': zone['id']
        }
        if zone['name'] in (cf_freeplans):
            pass
        else:
            zone_info.append(zone_data)
    return zone_info


def http_request(uri):
    headers = {"Authorization": "Bearer %s" % cf_token}
    addr = cf_api_url
    url = "{}/{}".format(addr, uri)
    r = requests.get(url, headers=headers)
    return json.loads(r.text)


def parse_cf_output(zone_name, data):
    #
    cf_requests = data['result']['totals']['requests']
    requests_all = cf_requests['all']
    requests_cached = cf_requests['cached']
    requests_unchached = cf_requests['uncached']
    bandwidth = data['result']['totals']['bandwidth']
    bandwidth_all = bandwidth['all']
    bandwidth_cached = bandwidth['cached']
    bandwidth_uncached = bandwidth['uncached']
    threats = data['result']['totals']['threats']
    threats_all = threats['all']
    unique = data['result']['totals']['uniques']
    unique_all = unique['all']
    pageviews = data['result']['totals']['pageviews']
    pageviews_all = pageviews['all']
    #
    ijt.json_template_cf_zone(zone_name, requests_all, requests_cached,
                         requests_unchached, bandwidth_all, bandwidth_cached,
                         bandwidth_uncached, threats_all, unique_all, pageviews_all)    
    countries = data['result']['totals']['requests']['country']
    ijt.json_template_cf_country(zone_name, countries)
    #
    http_status = data['result']['totals']['requests']['http_status']
    ijt.json_template_cf_http_status(zone_name, http_status)
    #




def fetch_analytics_by_zone():
    interval = datetime.datetime.now() - datetime.timedelta(seconds=fetch_interval)
    interval_window = interval.strftime("%Y-%m-%dT%H:%M:%SZ")
    for zone in cf_zone_info():
        zone_name = zone['zone_name']
        zone_id = zone['zone_id']
        uri = cf_analytics_uri_prefix.format(id=zone_id, interval=interval_window)
        zone_info = http_request(uri)
        print("Retrieving: {}".format(zone_name))
        parse_cf_output(zone_name, zone_info)


if __name__ == '__main__':
    sec_to_min = fetch_interval // 60
    while True:
        fetch_analytics_by_zone()
        time.sleep(sec_to_min)



