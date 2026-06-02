import tkinter as tk
from tkinter import filedialog
import random
from Experiment_Launcher_code.ModuleConfiguration import __USE_ARDUINO_SIM
if __USE_ARDUINO_SIM:
    from Arduino_related_code.ArduinoDigitalSim import *
else:
    from Arduino_related_code.ArduinoDigital import *

from Arduino_related_code.ValveControl import ValveControl
import Data_analysis.FileUtilities as fUtile
from Video_analyser_code.VimbaCameraController import VimbaCameraController
import cv2
from Video_analyser_code.VideoWriter import VideoWriter
import time


#instanciate valve object
def start_test():
    global valve_control
    global cycle_count, duration1_count, duration2_count
    global cam, video_writer

    cycle_count=duration1_count=duration2_count= 0
    valve_control = ValveControl(int(pin_entry.get()))



    # Force file selection
    filename = ''
    while filename == '' :
        filename = filedialog.asksaveasfilename(initialdir=fUtile.get_project_directory(),
                                 defaultextension=".avi", filetypes=[("AVI video", "*.avi")])
    video_writer = VideoWriter(output_file=filename, fps=50)
    cam = VimbaCameraController(50)
    cam.start_video()
    monitor_flow()

def monitor_flow():
    global cycle_count, duration1_count, duration2_count
    global cycle_time, video_writer

    # time to start a new cycle
    if cycle_time == 0:
        cycle_time = time.time()
        cycle_count += 1
        print(f"current cycle = {cycle_count}")
        if random.random() * 100 < int(probability_entry.get()):
            open_time = int(duration1_entry.get()) / 1000  # Convert duration from milliseconds to seconds
            duration1_count += 1
        else:
            open_time = int(duration2_entry.get()) / 1000
            duration2_count += 1
        valve_control.OpenValve(open_time)  # Open valve for the specified duration in seconds
        print(f"Valve opened for {open_time * 1000} milliseconds")

    #wait for end of cycle
    if time.time() - cycle_time > int(cycle_time_entry.get()):
        if valve_control.IsValveOpen():
            print(f"Error: Cycle time is too short")
            exit()
        cycle_time = 0

    if cycle_count < int(cycle_number_entry.get()):
        frame = cam.get_frame()
        if frame is not None:
            frame_image = frame.as_opencv_image()  # .copy()
            cv2.imshow('MouseCam', frame_image)
            cv2.waitKey(1)  # allow imshow() to manage the window. -> Looks like TK is covering for it.
            cam.free_frame(frame)  # return the buffer to the camera controller
            video_writer.write_frame(frame_image)
        root.after(1, monitor_flow)
    else:   # test done
        # Close the video writer and any other resources
        cam.close_resources()
        video_writer.close()
        cv2.destroyAllWindows()
        print(f"Number of duration 1 cycles = {duration1_count}")
        print(f"Number of duration 2 cycles = {duration2_count}")

# Initialize the ArduinoDigital object
comport = "COM11"
arduino = openComPort(comport)

# Initialize video system
can = None
cv2.namedWindow('MouseCam', cv2.WINDOW_NORMAL)
video_writer = None

# Setting up the Tkinter window
root = tk.Tk()
root.title("Water Flow Monitor")

# Creating input fields for pin number and duration
pin_label = tk.Label(root, text="Pin Number")
pin_label.pack()
pin_entry = tk.Entry(root)
pin_entry.pack()

cycle_time_label = tk.Label(root, text="Cycle time [Seconds]")
cycle_time_label.pack(pady=(5, 0))
cycle_time_entry = tk.Entry(root)
cycle_time_entry.pack()

duration1_label = tk.Label(root, text="First Duration (millisec)")
duration1_label.pack(pady=(5, 0))
duration1_entry = tk.Entry(root)
duration1_entry.pack()
duration1_count = 0

duration2_label = tk.Label(root, text="Second Duration (millisec)")
duration2_label.pack(pady=(5, 0))
duration2_entry = tk.Entry(root)
duration2_entry.pack()
duration2_count = 0

probability_label = tk.Label(root, text="First duration probability [%]")
probability_label.pack(pady=(5, 0))
probability_entry = tk.Entry(root)
probability_entry.pack()

cycle_number_label = tk.Label(root, text="Number Of Cycles")
cycle_number_label.pack(pady=(5, 0))
cycle_number_entry = tk.Entry(root)
cycle_number_entry.pack()
cycle_count = 0

# Button to start calibration
start_button = tk.Button(root, text="Start Test", command=start_test)
start_button.pack(pady=5)

# Start the GUI event loop
valve_control: ValveControl = None
cycle_time = 0
root.mainloop()


