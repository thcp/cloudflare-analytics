from influx_connect import influxdb_publish


def json_template_cf_zone(zone_name, requests_all, requests_cached,
                          requests_uncached, bandwidth_all, bandwidth_cached,
                          bandwidth_uncached, threats_all, unique_all, pageviews_all
                          ):
    template = [
        {
            "measurement": "cloudflare_analytics",
            "tags": {
                "zone": "",
            },
            "fields": {
                "requests_all": 0,
                "requests_cached": 0,
                "requests_unchached": 0,
                "bandwidth_all": 0,
                "bandwidth_cached": 0,
                "bandwidth_uncached": 0,
                "threats_all": 0,
                "unique_all": 0,
                "pageviews_all": 0
            }
        }
    ]
    template[0]['tags']['zone'] = zone_name
    template[0]['fields']['requests_all'] = requests_all
    template[0]['fields']['requests_cached'] = requests_cached
    template[0]['fields']['requests_unchached'] = requests_uncached
    template[0]['fields']['bandwidth_all'] = bandwidth_all
    template[0]['fields']['bandwidth_cached'] = bandwidth_cached
    template[0]['fields']['bandwidth_uncached'] = bandwidth_uncached
    template[0]['fields']['threats_all'] = threats_all
    template[0]['fields']['unique_all'] = unique_all
    template[0]['fields']['pageviews_all'] = pageviews_all
    influxdb_publish(template)


def json_template_cf_country(zone_name, countries):
    template = [
        {
            "measurement": "cloudflare_analytics_access_by_country",
            "tags": {
                "zone": "",
                "country": ""
            },
            "fields": {
                "visit_count": 0,
            }
        }
    ]
    for country in countries:
        template[0]['tags']['zone'] = zone_name
        template[0]['tags']['country'] = country
        template[0]['fields']['visit_count'] = countries[country]
        influxdb_publish(template)
        
def json_template_cf_http_status(zone_name, http_status):
    template = [
        {
            "measurement": "cloudflare_analytics_http_status_by_zone",
            "tags": {
                "zone": "",
                "http_status": "",
            },
            "fields": {
               "status_count": 0
            }
        }
    ]
    for code in http_status:
        template[0]['tags']['zone'] = zone_name
        template[0]['tags']['http_status'] = code
        template[0]['fields']['status_count'] = http_status[code]
        influxdb_publish(template)