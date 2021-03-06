#!/usr/bin/env python3

"""A MQTT to InfluxDB Bridge

This script receives MQTT data and saves those to InfluxDB.

"""

import os
import re
from typing import NamedTuple

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = os.getenv('INFLUXDB_HOST', 'influxdb.default')
#INFLUXDB_USER = 'root'
#INFLUXDB_PASSWORD = 'root'
INFLUXDB_DATABASE = os.getenv('INFLUXDB_DBNAME', 'home_sensors')

MQTT_ADDRESS = os.getenv('MQTT_HOST', 'mqtt.default')
#MQTT_USER = 'mqttuser'
#MQTT_PASSWORD = 'mqttpassword'
MQTT_TOPIC = 'home/sensors/+/+'  # home/sensors/<iddentifier>/<measure_name>
MQTT_REGEX = 'home/sensors/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = os.getenv('MQTT_CLIENT_ID', 'MQTTInfluxDBBridge')

#influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086)


class SensorData(NamedTuple):
    #location: str
    identifier: str
    measurement: str
    value: float


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)


def _parse_mqtt_message(topic, payload):
    match = re.match(MQTT_REGEX, topic)
    if match:
        #location = match.group(1)
        identifier = match.group(1)
        measurement = match.group(2)
        if measurement == 'status':
            return None
        return SensorData(identifier, measurement, float(payload))
    else:
        return None


def _send_sensor_data_to_influxdb(sensor_data):
    json_body = [
        {
            'measurement': sensor_data.measurement,
            'tags': {
                #'location': sensor_data.location
                'identifier': sensor_data.identifier
            },
            'fields': {
                'value': sensor_data.value
            }
        }
    ]
    influxdb_client.write_points(json_body)


def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)


def main():
    _init_influxdb_database()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    #mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
