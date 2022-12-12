import time

import paho.mqtt.client as mqtt_client
import random
from statistics import mean

import serial

buffer = []

my_id = 618


def get_connection(port):
    ser = serial.Serial(port, timeout=1)
    return ser


def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    topic = str(message.topic.encode("utf-8"))
    print(f"Received message on {topic}: {data}")
    buffer.append(int(data))
    if len(buffer) > 100:
        buffer.pop(0)
        if mean(buffer[:50]) > mean(buffer[50:]):
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

ser = get_connection('/dev/ttyUSB0')

time.sleep(600)
client.disconnect()
client.loop_stop()
print('Stop communication')
