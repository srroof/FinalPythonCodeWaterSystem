import serial
import datetime
from multiprocessing import Process
import pyMultiSerial as p

dateTime = str(datetime.datetime.now())
id1 = '/dev/ttyUSB0'
id2 = '/dev/ttyUSB1'
sensor1 = 18
sensor2 = 16
ms = p.MultiSerial()
ms.baudrate = 9600
ms.timeout = 2

if __name__ == '__main__':
    ms.Start()

    while True:
        number = serial.read()
        if number != b'':
            if int.from_bytes(number, byteorder='big') == 18:
                ser1 = serial.Serial(id1, 9600, timeout=1)  # start init for the first sensor
                ser1.reset_input_buffer()
                print("Water Pressure Sensor Found")
                ard1()
            if int.from_bytes(number, byteorder='big') == 16:
                ser2 = serial.Serial(id2, 9600, timeout=1)  # start init for the second sensor
                ser2.reset_input_buffer()
                print("Ground Water Content Sensors Found")
                ard2()
            else:
                print("No Identification Number Found")

    # ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    # ser.reset_input_buffer()
    # while True:
    #     if ser.in_waiting > 0:
    #         line = ser.readline().decode('utf-8').rstrip()
    #         lineScaled = str(line)  # scaling the input in
    #         print(lineScaled)
    #         print(dateTime)
    #         exit()


def ard1():
    serial.Serial(ser1, 9600, timeout=1)  # start init for the second sensor
    ser1.reset_input_buffer()
    line = ser.readline().decode('utf-8').rstrip()
    if line != '':
        lineInt = int(line)
        sensor1scaled = str(lineInt / 5)  # print into window to check variables and or send
        print("Amount of water being detected:")
        print(int(sensor1scaled))
        with open('WaterPressure.txt', 'w') as f:
            f.write(dateTime)  # write to text file
            f.write(lineScaled + "\n")
        ard2()


def ard2():  # for groundwater content monitoring / other sensors
    serial.Serial(ser2, 9600, timeout=1)  # start init for the second sensor
    ser2.reset_input_buffer()
    line = ser.readline().decode('utf-8').rstrip()
    if line != '':
        lineInt = int(line)
        sensor2scaled = str(lineInt / 2)  # print into window to check variables and or send
        print("Ground water being detected:")
        print(int(sensor2scaled))
        with open('GroundWater.txt', 'a') as f:
            f.write(dateTime)  # write to text file
            f.write(lineScaled + "\n")
        ard1()
