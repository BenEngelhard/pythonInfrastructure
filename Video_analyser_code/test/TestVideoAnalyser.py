import tkinter as tk
import time
from tkinter import filedialog
from tkinter import messagebox
from Video_analyser_code.VideoAnalyser import Video_Analyzer
import Data_analysis.FileUtilities as fUtile
import Data_analysis.CodeProfiler as Profiler


def browse_project_directory():
    global project_directory_var
    pd =  filedialog.askdirectory(title="Select a directory")
    project_directory_var.set(pd)

def stop_test():
    global stop_test_clicked
    stop_test_clicked = True

def start_test():
    global stop_test_clicked
    global project_directory_var
    global video_analyzer

    if not fUtile.set_project_directory(project_directory_var.get()):
        messagebox.showerror("Invalid Input", "Project Directory Does not Exist")
        return

    if not fUtile.set_experiment_directory('VideoTest'):
        return

    fUtile.set_experiment_directory('Exp1')
    if not fUtile.configure_mouse_directory('1', '2'):
        return
    fUtile.set_session_directory('session', '1')

    video_analyzer = Video_Analyzer()
    video_analyzer.start_video()
    start_button.after(3, timer_event)

def process_frame():
    global video_analyzer
    global stop_test_clicked
    global window

    if stop_test_clicked:
        window.destroy()
    else:
        Profiler.NewFrame()
        try:
            Profiler.EnterFunction('Process Single Frame')
            video_analyzer.process_single_frame()
            Profiler.ExitFunction('Process Single Frame')

        except Exception as e:
            print(f"Process frame raised an error event: {e}")

def timer_event():
    process_frame()
    start_button.after(10, timer_event)

# Run the test (at module level)
window = tk.Tk()
window.title("Video Analyzer Test")
window.geometry("550x200")

project_directory_var = tk.StringVar(value=None)
tk.Label(window, text="Project Directory:").place(x=5, y=60)
pd_name_entry = tk.Entry(window, width=60, textvariable=project_directory_var)
pd_name_entry.place(x=110, y=60)
pd_button = tk.Button(window, text="Browse", command=browse_project_directory)
pd_button.place(x=490, y=60)
start_button = tk.Button(window, text="Start Experiment", command=start_test)
start_button.place(x=150, y=120)
stop_button = tk.Button(window, text="Stop Experiment", command=stop_test)
stop_button.place(x=300, y=120)

project_directory_var.set(fUtile.get_project_directory())

stop_test_clicked = False
video_analyzer = None

window.mainloop()

# close and release
video_analyzer.close_resources()
