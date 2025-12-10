from Experiment_Launcher_code.ModuleConfiguration import __USE_ARDUINO_SIM

if __USE_ARDUINO_SIM:
    import Arduino_related_code.ArduinoDigitalSim as Arduino
else:
    import Arduino_related_code.ArduinoDigital as Arduino
import time
import numpy as np
from Data_analysis.HeartBeatLogger import HeartBeatLogger

class HeartBeat:
    def __init__(self, DigitalChannel, mean_period_milliSec):
        self.arduino_pin = DigitalChannel
        self.mean_period_milliSec = mean_period_milliSec
        self.next_heartbeat_time = HeartBeat.time_of_next_event(self.mean_period_milliSec, 10, 150)
        self.logger = HeartBeatLogger()
        self.logger.start_logging()
        self.start_time = 0

    def start(self, session_start_time):
        self.start_time = session_start_time

    def stop(self):
        self.logger.finalize_logging()

    def generate_heartbeat(self):
        if time.time() - self.next_heartbeat_time > 0:
            time_stamp = time.time() - self.start_time
            Arduino.DigitalHighPulse(self.arduino_pin, int(3))  # Start High pulse, time is given in mSec
            self.logger.log_data(time_stamp)
            self.next_heartbeat_time = HeartBeat.time_of_next_event(self.mean_period_milliSec, 10, 150)

    @staticmethod
    def time_of_next_event(mean, low, high):
        random_component = np.random.exponential(scale=mean - low)
        heartbeat_period = random_component + low
        if heartbeat_period > high:
            heartbeat_period = high
        return time.time() + heartbeat_period / 1000  # time is in seconds