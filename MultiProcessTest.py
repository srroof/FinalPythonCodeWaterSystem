import pyMultiSerial as p

# Create object of class pyMultiSerial
ms = p.MultiSerial()

ms.baudrate = 9600
ms.timeout = 2

#Add Callbacks
#Callback functions provide you an interface to perform an action at certain event.
# Callback function on detecting a port connection.
# Parameters: Port Number, Serial Port Object
# Return: True if the port is to be accepted, false if the port is to be rejected based on some condition

def port_connection_found_callback(portno, serial):
    print ("Port Found: "+portno)


#register callback function
ms.port_connection_found_callback = port_connection_found_callback


# Callback on receiving port data
# Parameters: Port Number, Serial Port Object, Text read from port
def port_read_callback(portno, serial, text):
    print("Received '"+ text +"' from port "+portno)
    serial.reset_input_buffer()
    line = ser.readline().decode('utf-8').rstrip()
    if line != '':
        lineInt = int(line)
        sensor1scaled = str(lineInt / 5)  # print into window to check variables and or send
        print("Amount of water being detected:")
        print(int(sensor1scaled))
        with open('WaterPressure.txt', 'w') as f:
            f.write(dateTime)  # write to text file
            f.write(lineScaled + "\n")
    pass

#register callback function
ms.port_read_callback = port_read_callback

                                                                                                               22,0-1        Top
