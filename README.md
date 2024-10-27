# GPS to MQTT
This project reads GPS data from a GPSD daemon and publishes it to an MQTT broker. It uses a systemd service to run the Python script automatically on boot. The configuration, including MQTT topics, is managed through a JSON file.

## Import Explanations
- **os**: System operations and file management.
- **json**: Loading configuration from a JSON file.
- **paho.mqtt.client as mqtt**: Publishing GPS data to an MQTT broker.
- **gpsd**: Fetching GPS data from the GPSD daemon.
- **pytz**: Converting time to the appropriate time zone.
- **from datetime import datetime**: Processing and formatting dates and times.


## Setup
1. Create venv
```sh
python3 -m venv gps-venv
source gps-venv/bin/activate
```
2. Install requirments.txt
```sh
pip install -r requirements.txt
```
3. Create the gps2mqtt.service in /etc/systemd/system/
4. Configure and start gps2mqtt systemd service: 
```sh
sudo systemctl daemon-reload
sudo systemctl enable gps2mqtt.service
sudo systemctl start gps2mqtt.service
sudo systemctl status gps2mqtt.service
```
5. Add topics to **.json** file


## Info
How to restart service?:
```sh
sudo systemctl daemon-reload
sudo systemctl restart gps2mqtt.service
```



I decided to enter coorditans on a rail to test the performance of the code.
From the page [Overpass](https://overpass-turbo.eu/) I downloaded a .json file with the coordinates of the Aragon track


