from __future__ import print_function
import pyMultiSerial as p
import serial
import qwiic_bme280
import sys
import datetime
import time
import requests

# Create object of class pyMultiSerial
ms = p.MultiSerial()
ms.baudrate = 9600
ms.timeout = 2


# Add Callbacks
# Callback functions provide you an interface to perform an action at certain event.
# Callback function on detecting a port connection.
# Parameters: Port Number, Serial Port Object
# Return: True if the port is to be accepted, false if the port is to be rejected based on some condition

def port_connection_found_callback(portno, serial):
    print("Port Found: " + portno)


# register callback function
ms.port_connection_found_callback = port_connection_found_callback


# Callback on receiving port data
# Parameters: Port Number, Serial Port Object, Text read from port
def port_read_callback(portno, serial, text):
    mySensor = qwiic_bme280.QwiicBme280()
    date = str(datetime.datetime.now())
    print(text + " at: " + date + " from port: " + portno)
    time.sleep(2)
    if not mySensor.connected:
        print("The Qwiic BME280 device isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    mySensor.begin()
    print("Humidity:\t%.3f" % mySensor.humidity)
    print("Pressure:\t%.3f" % mySensor.pressure)
    print("Temperature:\t%.2f" % mySensor.temperature_fahrenheit)
    time.sleep(2)

    with open('GroundWater.txt', '+a') as f:
        f.write(date)
        f.write("Humidity:\t%.3f" % mySensor.humidity + "\n")
        f.write("Pressure:\t%.3f" % mySensor.pressure + "\n")
        f.write("Temperature:\t%.2f" % mySensor.temperature_fahrenheit + "\n")
        f.write("\n")
    with open('GroundWater.txt', '+a') as f:
        f.write(date)  # write to text file
        f.write(text + "\n")

    # dataList = [GMC1, GMC2, Pressure1, Pressure2]
    # x = f.read(80)
    # if x == "GMC1":
    #     dataList[0] = f.readline()
    # if x == "GMC2":
    #     dataList[1] = f.readline()
    # if x == "Pressure1":
    #     dataList[2] = f.readline()
    # if x == "Pressure2":
    #     dataList[3] = f.readline()
    # pass


# def send_emoncms(dataList):
#
#     r = requests.post('http://172.31.171.113/input/post?node=emontx&fulljson=', json={
#         "GMC1": dataList[0],
#         "GMC2": dataList[1],
#         "Pressure 1": dataList[2],
#         "Pressure 2": dataList[3]
#     })
#     print(f"Status Code: {r.status_code}, Response: {r.json()}")


# register callback function
ms.port_read_callback = port_read_callback


# Callback on port disconnection. Triggered when a device is disconnected from port.
# Parameters: Port No
def port_disconnection_callback(portno):
    print("Port " + portno + " disconnected")


# register callback function
ms.port_disconnection_callback = port_disconnection_callback

# Start Monitoring ports
ms.Start()

