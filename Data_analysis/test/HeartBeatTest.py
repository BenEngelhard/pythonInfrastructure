from Experiment_Launcher_code.ModuleConfiguration import __USE_ARDUINO_SIM
if __USE_ARDUINO_SIM:
    import Arduino_related_code.ArduinoDigitalSim as Arduino
else:
    import Arduino_related_code.ArduinoDigital as Arduino

from Data_analysis.HeartBeat import HeartBeat
import time

# Initialize the ArduinoDigital object
comport = "COM11"
Arduino.openComPort(comport)

#initialize heart beat class
beat = HeartBeat(4, 30)

# Generate heart beat signals
start_time = time.time()
previous_pulse_time = start_time
pulse_counter = 0
total_periods = 0

while time.time() - start_time < 10:  # test duration is 10 seconds
    pulse_time =  beat.generate_heartbeat()
    if pulse_time > 0:
        period = pulse_time - previous_pulse_time
        pulse_counter += 1
        total_periods += period
        print(f'Heart beat pulse generated. Time: {int(period * 1000)}')
        previous_pulse_time = pulse_time
print(f'Average event period = {total_periods / pulse_counter * 1000:.2f}')