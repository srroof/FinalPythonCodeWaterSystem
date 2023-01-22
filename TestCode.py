import serial
import requests
import datetime

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            linep = str (line)
            print(linep)
            dateAud1 = datetime.datetime.now()
            print(dateAud1)
            # requests.get(http://192.168.42.1/input/post?node = emontx & fulljson = {"power1": 250, "power2": 500, "power3": 300, "time": "2021-07-21T15%3A51%3A26%2B01%3A00"})

            # http: // 192.168.42.1 / input / post?node = emontx & fulljson = {"power1": 100, "power2": 200, "power3": 300,"time": "2021-07-21T16%3A08%3A14%2B01%3A00"}


