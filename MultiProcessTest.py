import pyMultiSerial as p
import serial
import datetime
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
    date = str(datetime.datetime.now())
    print(text + " at: " + date + " from port: " + portno)
    with open('GroundWater.txt', '+a') as f:
        f.write(dateTime)  # write to text file
        f.write(text + "\n")
    dataList = [GMC1, GMC2, Pressure1, Pressure2]
    x = f.read(20)
    if x == "GMC1":
        dataList[0] = f.readline()
    if x == "GMC2":
        dataList[1] = f.readline()
    if x == "Pressure1":
        dataList[2] = f.readline()
    if x == "Pressure2":
        dataList[3] = f.readline()
    pass


def send_emoncms(dataList):

    r = requests.post('http://172.31.171.113/input/post?node=emontx&fulljson=', json={
        "GMC1": dataList[0],
        "GMC2": dataList[1],
        "Pressure 1": dataList[2],
        "Pressure 2": dataList[3]
    })
    print(f"Status Code: {r.status_code}, Response: {r.json()}")


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

# To stop monitoring, press Ctrl+C in the console or command line.


# Caution: Any code written below ms.Start() will be executed only after monitoring is stopped.
# Make use of callback functions to execute your code.
