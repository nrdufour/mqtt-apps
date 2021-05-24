#!/usr/bin/env python3

"""A ZigBee (through MQTT) to MQTT Bridge

This script receives zigbee data via mqtt and send them back to MQTT
as expected by the mqtt-bridge :-)

"""

import os
import re
from typing import NamedTuple

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

MQTT_ADDRESS = os.getenv('MQTT_HOST', 'mqtt.default')
#MQTT_USER = 'mqttuser'
#MQTT_PASSWORD = 'mqttpassword'
MQTT_TOPIC = 'home/sensors/zigbee/raw/+'  # home/sensors/zigbee/raw/<iddentifier>
MQTT_REGEX = 'home/sensors/zigbee/raw/([^/]+)'
NEW_TOPIC_FORMAT = 'home/sensors/zb-{id}/{field}'
MQTT_CLIENT_ID = os.getenv('MQTT_CLIENT_ID', 'Zigbee2MQTT')
SHORT_2_CLEAN_NAMES = {
        'CT': 'control_temperature',
        'P':  'pressure',
        'H':  'humidity',
        'T':  'temperature',
        'LG': 'light'
        }


class SensorData(NamedTuple):
    identifier: str
    payload: str


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    if sensor_data is not None:
        _send_back_to_mqtt(sensor_data)


def _parse_mqtt_message(topic, payload):
    match = re.match(MQTT_REGEX, topic)
    if match:
        identifier = match.group(1)
        return SensorData(identifier, payload)
    else:
        return None

def clean_field_name(name):
    if name in SHORT_2_CLEAN_NAMES:
        return SHORT_2_CLEAN_NAMES[name]
    else:
        return name

def _send_back_to_mqtt(sensor_data):
    fields = sensor_data.payload.split(";")
    for f in fields:
        [name,value] = f.split("|")

        clean_name = clean_field_name(name)
        clean_value = value.strip()

        new_topic = NEW_TOPIC_FORMAT.format(
                id = sensor_data.identifier, 
                field = clean_name)
        print("About to send: ["+new_topic+"] == ["+clean_value+"]")
        publish.single(new_topic, clean_value, hostname=MQTT_ADDRESS)


def main():
    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    #mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('Zigbee to MQTT bridge')
    main()
