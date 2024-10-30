# Raspberry Pi GPS Projects Overview

This repository contains two distinct GPS-based projects for a Raspberry Pi, each serving a different purpose for handling and transmitting GPS data:

---

## 1. GPS USB Data Logger

### Description
This project continuously logs GPS data from a GPSD daemon to a JSON file on a USB pendrive. It uses a multithreaded Python script to ensure data logging is consistent, even if the USB drive is temporarily disconnected. The data is stored locally, making it ideal for offline use and data collection.

### Key Features
- Logs **latitude**, **longitude**, **altitude**, **speed**, and **satellite information**.
- Saves data as JSON entries on a USB drive.
- Automatically remounts the USB if disconnected.
- Can run as a systemd service for automatic startup on boot.

---

## 2. GPS to MQTT Publisher

### Description
This project publishes real-time GPS data to an MQTT broker, making it accessible for remote monitoring and integration with IoT platforms. It reads data from the GPSD daemon and publishes key GPS metrics, such as location, altitude, and satellite count, to configurable MQTT topics.

### Key Features
- Publishes GPS data (**location**, **altitude**, **track**, and **time**) to MQTT topics.
- Allows real-time data access and integration with other IoT systems.
- Configurable MQTT settings, including server address, topics, and client ID.
- Can run as a systemd service for automatic startup on boot.
