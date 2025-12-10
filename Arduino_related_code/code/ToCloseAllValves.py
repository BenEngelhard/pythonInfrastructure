from Arduino_related_code.ArduinoDigital import ArduinoDigital

# Replace 'COM3' with the appropriate port name your Arduino is connected to.
arduino = ArduinoDigital('COM11')

def setup():
    pins = [7,8, 9, 10, 11, 12]
    for pin in pins:
        arduino.DigitalLow(pin)

def loop():
    while True:
        # Add actions here to be repeated in the loop.
        pass

setup()
loop()
