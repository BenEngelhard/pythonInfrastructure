import tkinter as tk
import random
import time

from Experiment_Launcher_code.ModuleConfiguration import __USE_ARDUINO_SIM
if __USE_ARDUINO_SIM:
    from Arduino_related_code.ArduinoDigitalSim import *
else:
    from Arduino_related_code.ArduinoDigital import *

from Arduino_related_code.ValveControl import ValveControl
import time

class ValveEntry:
    def __init__(self):
        self.pin_number = tk.StringVar(value=None)
        self.opening_time = tk.StringVar(value=None)

def start_test():
    global valve_entries, valve_objects
    global cycle_time, cycle_count
    global cycle_number_entry

    cycle_time = 0
    cycle_count = 0
    valve_objects = []
    for entry in valve_entries:
        channel = int(entry.pin_number.get())
        if not channel == 0:
            obj = ValveControl(channel)
            valve_objects.append(obj)
        else:
            valve_objects.append(None)
    root.after(1, monitor_flow)

def monitor_flow():
    global cycle_time, cycle_count, valve_objects, valve_entries

    if cycle_time == 0:
        # time to start a new cycle
        cycle_time = time.time()
        cycle_count += 1
        print(f"current cycle = {cycle_count}")
        for i, obj in enumerate(valve_objects):
            if not obj is None:
                open_time = int(valve_entries[i].opening_time.get())
                obj.OpenValve(open_time / 1000) # convert to seconds
                print(f"Valve {i+1} opened for {open_time} milliseconds")

    #wait for end of cycle
    error_flag = False
    if time.time() - cycle_time > int(cycle_time_entry.get()):
        for inx, obj in enumerate(valve_objects):
            if not obj is None:
                if obj.IsValveOpen():
                    print(f"Error: Cycle time is too short for valve {inx +1}")
                    error_flag = True
        if error_flag:
            exit()
        else:
            cycle_time = 0

    # Check end of test
    if cycle_count < int(cycle_number_entry.get()):
        root.after(1, monitor_flow)
    else:   # test done
        print('Test Done')

# Main program
# Initialize the ArduinoDigital object
comport = "COM11"
arduino = openComPort(comport)

# Setting up the Tkinter window
root = tk.Tk()
root.title("Multi Valve Flow Monitor")
root.geometry("450x270")

# create 4 valve panel
valve_entries = []
valve_objects = []
for i in range(4):
    valve = ValveEntry()
    valve_panel = tk.Frame(root, width=100, height=150, relief=tk.RAISED, borderwidth=2)
    valve_panel.place(x=10 + (110 * i), y=10)
    tk.Label(valve_panel, text=f'Valve {i+1}').place(x=2, y=2)
    tk.Label(valve_panel, text="Pin Number").place(x=2, y=25)
    tk.Entry(valve_panel, textvariable=valve.pin_number, width = 7).place(x=10, y=50)
    valve.pin_number.set('0')
    tk.Label(valve_panel, text="Opening Time").place(x=2, y=75)
    tk.Entry(valve_panel, textvariable=valve.opening_time, width=7).place(x=10, y=100)
    tk.Label(valve_panel, text="[mSec]").place(x=5, y=120)
    valve_entries.append(valve)

cycle_panel = tk.Frame(root, width=430, height=50, relief=tk.RAISED, borderwidth=2)
cycle_panel.place(x=10, y=163)
tk.Label(cycle_panel, text='Cycles').place(x=2, y=2)
tk.Label(cycle_panel, text="Number Of Cycles:").place(x=30, y=20)
cycle_number_entry = tk.StringVar()
cycle_number_entry.set('0')

tk.Entry(cycle_panel, textvariable=cycle_number_entry, width = 7).place(x=140, y=20)

tk.Label(cycle_panel, text="Cycle time [Seconds]:").place(x=220, y=20)
cycle_time_entry = tk.StringVar()
cycle_time_entry.set('0')
tk.Entry(cycle_panel, textvariable=cycle_time_entry, width = 7).place(x=350, y=20)

# Button to start calibration
start_button = tk.Button(root, text="Start Test", command=start_test)
start_button.place(x=200, y=230)

# Start the GUI event loop
cycle_time = 0
cycle_count = 0
root.mainloop()

