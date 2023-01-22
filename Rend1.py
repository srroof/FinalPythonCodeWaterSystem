import serial
import datetime
from multiprocessing import Process

id1 = '/dev/ttyUSB0'
id2 = '/dev/ttyUSB1'
sensor1 = 18
sensor2 = 16

if __name__ == '__main__':
    while True:
        number = ser.read()
        if number != b'':
            if int.from_bytes(number, byteorder='big') == 18:
                ser1 = serial.Serial(id1, 9600, timeout=1)     # start init for the first sensor
                ser1.reset_input_buffer()
                print("Water Pressure Sensor Found")
                Ad1
            if int.from_bytes(number, byteorder='big') == 16:
                ser2 = serial.Serial(id2, 9600, timeout=1)      # start init for the second sensor
                ser2.reset_input_buffer()
                print("Ground Water Content Sensors Found")
                Ad2
            else:
                print("No Identification Number Found")

    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            linep = str(line)                                           #scaling the input in
            print(linep)
            dateArd1 = str(datetime.datetime.now())
            print(dateArd1)

def Ard1():
        serial.Serial(ser1, 9600, timeout=1)  # start init for the second sensor
        ser1.reset_input_buffer()
        line = ser.readline().decode('utf-8').rstrip()
        if line != '':
            lineInt = int(line)
            lineScaled = str(lineInt / 5)
            dateAud1 = str(datetime.datetime.now())
            print(dateAud1)                                 # print into window to check variables and or send
            print("Amount of water being detected:")
            print(int(dataScaled))
            with open('WaterPressure.txt', 'w') as f:
                f.write(dateArd1)                           # write to text file
                f.write(lineScaled + "\n")
            # Ard2()


# def Ard2:  # for groundwater content monitoring / other sensors
#     while True:
#         ser2 = serial.Serial(id2, 9600, timeout=1)  # start init for the second sensor
#         ser2.reset_input_buffer()
#         line = ser.readline().decode('utf-8').rstrip()
#         if line != '':
#             lineInt = int(line)
#             lineScaled = str(lineInt / 2)
#             dateAud2 = str(datetime.datetime.now())
#             print(dateAud2)                                 # print into window to check variables and or send
#             print("Ground water being detected:")
#             print(int(lineScaled))
#             with open('GroundWater.txt', 'w') as f:
#                 f.write(dateAud2)                           # write to text file
#                 f.write(lineScaled + "\n")
#             Ad1()
