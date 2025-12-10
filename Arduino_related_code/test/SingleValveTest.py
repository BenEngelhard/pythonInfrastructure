from Arduino_related_code.ArduinoDigital import ArduinoDigital
import time

# Replace 'COM3' with the appropriate port name your Arduino is connected to.
arduino = ArduinoDigital('COM11')

def setup():
    pins = [7, 8, 9, 10, 11, 12]
    for pin in pins:
        arduino.DigitalLow(pin)
    time.sleep(3)  # Delay for 3 seconds (3000 milliseconds)

def loop():
    while True:
        arduino.DigitalHigh(9)#to open
        time.sleep(3)  # Delay for 3 seconds (3000 milliseconds)
        arduino.DigitalLow(9)#to close
        time.sleep(3)  # Delay for 3 seconds (3000 milliseconds)

setup()
loop()
