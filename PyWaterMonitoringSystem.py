from __future__ import print_function  **What is this? Doesn't seem to be used
import paho.mqtt.publish as publish
import pyMultiSerial as p   # Create object of class pyMultiSerial
import serial
import qwiic_bme280
import sys
import datetime
import time
import requests    **Not needed if you use mqtt


ms = p.MultiSerial()
ms.baudrate = 9600  # open serial port at 9600 to match Arduino's
ms.timeout = 2  # time it will take to retrieve data from the ports that are open
date = str(datetime.datetime.now())


# Callback function on detecting a port connection.
# Parameters: Port Number, Serial Port Object
# Return: True if the port is to be accepted, false if the port is to be rejected based on some condition within library

# Check if there are any ports open and if so continue
def port_connection_found_callback(portno, serial):
    print("Port Found: " + portno)


# register callback function
ms.port_connection_found_callback = port_connection_found_callback


# Callback on receiving port data
# Parameters: Port Number, Serial Port Object, Text read from port
def port_read_callback(portno, serial, text):
    print(text)  # pull text from the port and print it for debugging purposes
    time.sleep(2)  # force slowdown so pi doesn't get backed up and crash

    with open('GroundWater.txt', '+a') as f:  # write data to file GroundWater.txt stored on the pi
        f.write(date)  # write to text file
        f.write(text + "\n")

    # here im going to parse the text data coming in and turn it into ints then scale as necessary. Some data
    # is already scaled in the Arduino's such as percentages because it's not a lot of load for the arduino
    with open('portread.txt', '+w') as r:  # Open new file to store data only for each call back in order to read   **Why do you need to write 'text' to disk?
        r.write(text + "\n")        # writing data to file without appending
        readline = r.readline()
        read = readline[0: 4]     # read the first 4 characters of the file to get the pointer to the data

        # using the pointer set the correct data set to the data following the pointer
        if read == "gmc1":
            gmc1 = readline[4: 10]
        if read == "gmc2":
            gmc2 = readline[4: 10]
        if read == "pre1":
            pre1 = readline[4: 10]
        if read == "pre2":
            pre2 = readline[4: 10]
        else:  # if no data found then return out and look for more
            print("No data was found. looking for more")

    breakout_sensor()  # calls for function breakout sensor  ** This will get called every time an Arduino sends data. Would it make more sense to call this on a time interval? But maybe you can't once ms.Start() is called?

    # calls for function breakout sensor while sending the data in as args
    emon_send(gmc1, gmc2, pre1, pre2, humidity, atm_pressure, temperature)   **I think your group of 'if' statements above will only define one of gmc1, gmc2, etc. The others will be undefined and thus cause a problem here 


# register callback function
ms.port_read_callback = port_read_callback


# Callback on port disconnection. Triggered when a device is disconnected from port.
# Parameters: Port No
def port_disconnection_callback(portno):
    print("Port " + portno + " disconnected")


# register callback function
ms.port_disconnection_callback = port_disconnection_callback


def breakout_sensor():
    mySensor = qwiic_bme280.QwiicBme280()
    mySensor.begin()  # start atm breakout sensor
    if mySensor.connected:
        humidity = ("Humidity:\t%.3f" % mySensor.humidity)  # find humidity  **I think that 'humidity', 'atm_pressure', etc are local variables only valid inside this function. You need to define them as global - see https://www.w3schools.com/python/python_variables_global.asp
        atm_pressure = ("Pressure:\t%.3f" % mySensor.pressure)  # find atmospheric pressure
        temperature = ("Temperature:\t%.2f" % mySensor.temperature_fahrenheit)  # find temperature
        time.sleep(2)  # force slowdown so pi doesn't get backed up and crash
        print(humidity, atm_pressure, temperature)  # print for debugging purpose
        with open('atmBreakout.txt', '+a') as f:  # write text to file with append
            f.write(date)
            f.write(humidity + "\n")
            f.write(atm_pressure + "\n")
            f.write(temperature + "\n")
            f.write("\n")
        return
    if not mySensor.connected:
        print("The Qwiic BME280 device isn't connected to the system. Please check your connection",
              file=sys.stderr)
        return


# send data to Emoncms using data put into dictionary (key-value pairs)
def emon_send(gmc1, gmc2, pre1, pre2, humidity, atm_pressure, temperature):
    thisdict = {
        "ground moisture 1": gmc1,
        "ground moisture 2": gmc2,
        "Water Pressure 1": pre1,
        "Water Pressure 2": pre2,
        "Humidity": humidity,
        "Atmospheric Pressure": atm_pressure
    }
    print(thisdict)

    # Finalized readings to send to Emon
    moisture1 = gmc1
    moisture2 = gmc2
    pressure1 = pre1
    pressure2 = pre2
    GPM1 = 211
    Temperature1 = temperature
    Rotation1_RPM = 0.3

    # publish multiple messages - this is a Python list of dict elements!
    # topic parts: "emon" is required; "Sprinkler1" is a Node-name; "Moisture1" "GPM1", etc. are data labels
    msg = [{'topic': "emon/Sprinkler1/Moisture1", 'payload': moisture1},
           {'topic': "emon/Sprinkler1/Moisture2", 'payload': moisture2},
           {'topic': "emon/Sprinkler1/Pressure1", 'payload': pressure1},
           {'topic': "emon/Sprinkler1/Pressure2", 'payload': pressure2},
           {'topic': "emon/Sprinkler1/GPM1", 'payload': GPM1},
           {'topic': "emon/Sprinkler1/Temperature1", 'payload': Temperature1},
           {'topic': "emon/Sprinkler1/Rotation1_RPM", 'payload': Rotation1_RPM}]

    # Publish them via MQTT using the multiple method
    # Do not need to specify a host since publishing internally
    publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})
    return


# Start Monitoring ports
ms.Start()

# Any code written below ms.Start() will be executed only after monitoring is stopped.
