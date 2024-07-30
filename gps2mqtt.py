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

# MQTT client configuration
client = mqtt.Client(client_id=mqtt_client_id, protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_publish = on_publish

try:
    client.connect(mqtt_server, mqtt_port, 60)
    client.loop_start()  # Starts the background processing loop
except Exception as e:
    print(f"Error connecting to MQTT broker: {e}")
    exit(1)
