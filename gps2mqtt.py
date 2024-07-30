import os
import json
import paho.mqtt.client as mqtt
import gpsd
import pytz
from datetime import datetime

config_path = 'config.json'
with open(config_path) as config_file:
    config = json.load(config_file)

mqtt_server = config['mqtt']['server']
mqtt_port = config['mqtt']['port']
mqtt_client_id = config['mqtt']['clientIdentifier']
mqtt_topics = config['mqtt']['topics']

gpsd.connect()
