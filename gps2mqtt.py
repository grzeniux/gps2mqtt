import os
import json
import paho.mqtt.client as mqtt
import gpsd
import pytz
from datetime import datetime

class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"Location(latitude={self.latitude}, longitude={self.longitude})"

# Load configuration from JSON file
config_path = 'config.json'
with open(config_path) as config_file:
    config = json.load(config_file)

mqtt_server = config['mqtt']['server']
mqtt_port = config['mqtt']['port']
mqtt_client_id = config['mqtt']['clientIdentifier']
mqtt_topics = config['mqtt']['topics']

gpsd.connect()

# Callback functions to debug an MQTT connection
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT broker.")
    else:
        print(f"Failed to connect to MQTT broker. Return code: {rc}")

def on_publish(client, userdata, mid):
    print(f"Data published. Message ID: {mid}")

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

def publish_gps_data():
    try:
        gpsd_data = gpsd.get_current()
        if gpsd_data.mode >= 2:
            location = Location(gpsd_data.lat, gpsd_data.lon)

            altitude = gpsd_data.alt  # height
            track = gpsd_data.track  # Direction of movement in degrees
            sats = gpsd_data.sats  # Number of visible satellites
            time_utc = gpsd_data.time  # UTC time

            # Converting time to CET/CEST (Central European Summer/Winter Time) zone.
            utc_dt = datetime.strptime(time_utc, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.utc)
            cest = pytz.timezone('Europe/Warsaw')
            time_cest = utc_dt.astimezone(cest).strftime('%Y-%m-%d %H:%M:%S')

            if location.latitude and location.longitude:
                client.publish(mqtt_topics['latitude'], location.latitude)
                client.publish(mqtt_topics['longitude'], location.longitude)
                client.publish(mqtt_topics['altitude'], altitude)
                client.publish(mqtt_topics['track'], track)
                client.publish(mqtt_topics['satellites'], sats)
                client.publish(mqtt_topics['time'], time_cest)

                print(f"Location: {location}")
                print(f"Altitude: {altitude}, Track: {track}, Satellites: {sats}")
                print(f"Time (CEST/CET): {time_cest}")

    except KeyError:
        pass
    except Exception as e:
        print(f"Error in publish_gps_data: {e}")

while True:
    publish_gps_data()
