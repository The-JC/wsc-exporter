# Coded via StarLink in the Australian Outback on 24.10.2023 by Julian Hellner(julian@hellner.cc)

from prometheus_client import start_http_server, Metric, REGISTRY
import json
import requests
import sys
import time

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = endpoint
  def collect(self):
    # Fetch the JSON
    response = requests.get(self._endpoint).json()

    metric = Metric('team_position','Team Position', 'gauge')

    for team in response['items']:
        team_num = team['teamnum']
        team_name = team['shortname'].lower()
        team_class = team['class'].lower()
        trailering = str(team['trailering']).lower()
        
        metric.add_sample('team_position_distance', value=team['distance'], labels={'teamnum': team_num, 'team': team_name, 'class': team_class, 'trailering':  trailering})

        metric.add_sample('team_position_latitude', value=team['latitude'], labels={'teamnum': team_num, 'team': team_name, 'class': team_class, 'trailering':  trailering})

        metric.add_sample('team_position_longitude', value=team['longitude'], labels={'teamnum': team_num, 'team': team_name, 'class': team_class, 'trailering':  trailering})
        metric.add_sample('team_position_altitude', value=team['altitude'], labels={'teamnum': team_num, 'team': team_name, 'class': team_class, 'trailering':  trailering})

        metric.add_sample('team_position_avg_speed', value=team['avg_speed'], labels={'teamnum': team_num, 'team': team_name, 'class': team_class, 'trailering':  trailering})
        metric.add_sample('team_position_speed', value=team['speed'], labels={'teamnum': team_num, 'team': team_name, 'class': team_class, 'trailering':  trailering})
    yield metric

    metric = Metric('team_state','Team State', 'gauge')

    for team in response['items']:
        team_num = team['teamnum']
        team_name = team['shortname'].lower()
        team_class = team['class'].lower()
        
        metric.add_sample('team_state_last_update', value=team['last'], labels={'teamnum': team_num, 'team': team_name, 'class': team_class, 'trailering':  trailering})
        
        metric.add_sample('team_state_trailering', value=team['trailering'], labels={'teamnum': team_num, 'team': team_name, 'class': team_class, 'trailering':  trailering})

        
    yield metric


if __name__ == '__main__':
  # Usage: json_exporter.py port endpoint
  port= 9000
  endpoint = 'https://telemetry.worldsolarchallenge.org/wscearth/api/positions'
  start_http_server(port)
  REGISTRY.register(JsonCollector(endpoint))

  while True: time.sleep(1)