import time

import paho.mqtt.client as mqtt_client
import random
from statistics import mean

import serial

buffer = []

my_id = 618

mn = 100
mx = 0

def get_connection(port):
    ser = serial.Serial(port, timeout=1)
    return ser


def on_message(client, userdata, message):
    global mx
    global mn
    data = message.payload
    topic = message.topic
    print(f"Received message on {topic}: {data}. min: {mn}, max: {mx}")

    if topic == "lab/%s/photo/max" % my_id:
        mx = int(data)

    if topic == "lab/%s/photo/min" % my_id:
        mn = int(data)

    if topic == "lab/%s/photo/stream" % my_id:
        if int(data) < (mn + mx) / 2:
            ser.write(bytearray([ord('1')]))
        else:
            ser.write(bytearray([ord('0')]))

broker = "broker.emqx.io"

client = mqtt_client.Client(f'isu_fbki_{random.randint(10000, 99999)}')
client.on_message = on_message

try:
    client.connect(broker)
except Exception:
    print('Failed to connect, check network')
    exit()

client.loop_start()

print('Subscribing')
client.subscribe("lab/%s/photo/stream" % my_id)
client.subscribe("lab/%s/photo/min" % my_id)
client.subscribe("lab/%s/photo/max" % my_id)

ser = get_connection('/dev/ttyUSB0')

time.sleep(600)
client.disconnect()
client.loop_stop()
print('Stop communication')
