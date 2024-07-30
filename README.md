# GPS to MQTT


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
