from Experiment_Launcher_code.ModuleConfiguration import __USE_ARDUINO_SIM
if __USE_ARDUINO_SIM:
    import Arduino_related_code.ArduinoDigitalSim as Arduino
else:
    import Arduino_related_code.ArduinoDigital as Arduino
import time

class ValveControl:
    def __init__(self, channel):
        self.channel = channel
        self.CloseValve()
        self.starttime = 0
        self.duration = 0
        self.valveopen = False

    def OpenValve(self, duration):
        if duration > 0:
            self.starttime = time.time()
            self.duration = duration
            Arduino.DigitalLowPulse(self.channel, int(duration * 1000))  # Start Low pulse, time is converted to mSec
            self.valveopen = True

    def CloseValve(self):
        Arduino.DigitalHigh(self.channel)  # Set the pin high
        self.valveopen = False

    def IsValveOpen(self):
        if self.valveopen:
            if time.time() - self.starttime > self.duration:
                self.valveopen = False
        return self.valveopen
