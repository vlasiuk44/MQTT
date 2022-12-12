import time

import paho.mqtt.client as mqtt_client
from statistics import mean
import serial

my_id = 618
values = []
initial = True


def get_connection(port):
    ser = serial.Serial(port, timeout=1)
    return ser


client = mqtt_client.Client()

broker = "broker.emqx.io"
try:
    client.connect(broker)
except Exception:
    print('Failed to connect, check network')
    exit()

ser = get_connection('/dev/ttyUSB0')

while True:
    if ser.in_waiting > 0:
        data = ser.read(1)
        print(data[0])
        client.publish("lab/%s/photo/instant" % my_id, data[0])
        if initial:
            values = [data[0] for i in range(100)]
            initial = False
        values.pop(0)
        values.append(data[0])
        client.publish("lab/%s/photo/averge" % my_id, mean(values))
    time.sleep(0.01)
