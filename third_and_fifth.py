import time

import paho.mqtt.client as mqtt_client
import serial

my_id = 618

interval = 100
do_calibrate = True

mn = 100
mx = 0

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

ser = get_connection('/dev/ttyACM0')
steps = 0

while True:
    if ser.in_waiting > 0:
        if ser.in_waiting >= 2 or interval <= 0:
            do_calibrate = False
            interval += 1
        print("In waiting: " + str(ser.in_waiting))
        data = ser.read(1)
        if mn > data[0]:
            mn = data[0]
        client.publish("lab/%s/photo/min" % my_id, mn)
        if mx < data[0]:
            mx = data[0]
        client.publish("lab/%s/photo/max" % my_id, mx)

        print("Value: " + str(data[0]))
        print("min: " + str(mn) + ", max: " + str(mx))
        client.publish("lab/%s/photo/stream" % my_id, data[0])
        ser.write(bytearray([int(ord("I")), int(interval)]))
        print("Interval: " + str(interval))
        if do_calibrate:
            if steps % 10 == 0:
                interval -= 1
        steps += 1
        print("==============\n")
