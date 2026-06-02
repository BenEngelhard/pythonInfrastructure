import tkinter as tk
from threading import Thread
from infrastructure.Arduino_related_code.ArduinoDigital import *
from infrastructure.Arduino_related_code.ValveControl import ValveControl
import time

def calibrate_valve(pin, duration_ms,opening_number):
    valve_control = ValveControl(pin)
    duration_s = duration_ms / 1000  # Convert duration from milliseconds to seconds
    time.sleep(4)

    for i in range(opening_number):
        print(f"Calibrating valve on pin {pin}: Iteration {i+1}")
        valve_control.OpenValve(duration_s)  # Open valve for the specified duration in seconds

        while valve_control.IsValveOpen():
           pass

        print(f"Valve on pin {pin} closed.")
        time.sleep(1)  # Short delay between iterations

# Initialize the ArduinoDigital object
comport = "COM11"
arduino = openComPort(comport)

# Setting up the Tkinter window
root = tk.Tk()
root.title("Valve Calibration")

# Creating input fields for pin number and duration
pin_label = tk.Label(root, text="Enter Pin Number:")
pin_label.pack()
pin_entry = tk.Entry(root)
pin_entry.pack()

duration_label = tk.Label(root, text="Enter Duration (millisec):")
duration_label.pack()
duration_entry = tk.Entry(root)
duration_entry.pack()

OpeningNumber_label = tk.Label(root, text="Enter number of times you want the valve to open and close:")
OpeningNumber_label.pack()
OpeningNumber_entry = tk.Entry(root)
OpeningNumber_entry.pack()

# Button to start calibration
calibrate_button = tk.Button(root, text="Start Calibration",
                             command=lambda: calibrate_valve(int(pin_entry.get()),
                                                               int(duration_entry.get()),int(OpeningNumber_entry.get())))

calibrate_button.pack()

# Start the GUI event loop
root.mainloop()


