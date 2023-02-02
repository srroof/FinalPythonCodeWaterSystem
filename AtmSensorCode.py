from __future__ import print_function
import qwiic_bme280
import time
import sys


def runExample():
    mySensor = qwiic_bme280.QwiicBme280()

    if mySensor.connected == False:
        print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
              file=sys.stderr)
        return

    mySensor.begin()

    while True:
        date = str(datetime.datetime.now())

        print("Humidity:\t%.3f" % mySensor.humidity)

        print("Pressure:\t%.3f" % mySensor.pressure)

        print("Temperature:\t%.2f" % mySensor.temperature_fahrenheit)

        print("")

        with open('GroundWater.txt', '+a') as f:
            f.write(date)
            f.write("Humidity:\t%.3f" % mySensor.humidity + "\n")
            f.write("Pressure:\t%.3f" % mySensor.pressure + "\n")
            f.write("Temperature:\t%.2f" % mySensor.temperature_fahrenheit + "\n")
            f.write("\n")
        time.sleep(1)


if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
sys.exit(0)
