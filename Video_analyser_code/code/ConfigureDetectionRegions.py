import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import Data_analysis.FileUtilities as fUtile


def populate_system_parameters_panel(panel, pdVar):
    tk.Label(panel, text="Project Directory:").place(x=5, y=10)
    pd_name_entry = tk.Entry(panel, width=60, textvariable=pdVar)
    pd_name_entry.place(x=110, y=10)
    pd_button = tk.Button(panel, text="Browse", command=browse_project_directory)
    pd_button.place(x=485, y=5)

def browse_project_directory():
    global project_directory_var, save_conf_bt
    directory_path = filedialog.askdirectory(title="Select a directory")
    if directory_path != "":
        project_directory_var.set(directory_path)
        save_conf_bt.config(state="normal")

def draw_detection_canvas(panel, title, X, Y, geometry):
    rwidth = 50 if geometry == 'n' else 100
    rheight = 100 if geometry == 'n' else 80
    titlex = 35 if geometry == 'n' else 55
    titley = 50 if geometry == 'n' else 45
    canvas = tk.Canvas(panel, width=rwidth, height=rheight, bg="white", bd=5, relief="ridge")
    canvas.create_text(titlex, titley, text=title, font=("Arial", 10, "bold"), fill="blue")
    canvas.place(x=X, y=Y)

def create_detection_set(panel, edit_vars, X, Y, geometry):
    xOffset = 120 if geometry == 'n' else 170
    yOffset = 115 if geometry == 'n' else 90

    tk.Label(panel, text="X:").place(x=X-55, y=Y-20)
    tk.Entry(panel, width=5, textvariable=edit_vars[0][0]).place(x=X-35, y=Y-20)
    tk.Label(panel, text="Y:").place(x=X-55, y=Y)
    tk.Entry(panel, width=5, textvariable=edit_vars[0][1]).place(x=X-35, y=Y)
    tk.Label(panel, text="X:").place(x=X-55+xOffset, y=Y-20+yOffset)
    tk.Entry(panel, width=5, textvariable=edit_vars[1][0]).place(x=X-35+xOffset, y=Y-20+yOffset)
    tk.Label(panel, text="Y:").place(x=X-55+xOffset, y=Y+yOffset)
    tk.Entry(panel, width=5, textvariable=edit_vars[1][1]).place(x=X-35+xOffset, y=Y+yOffset)

def start_video_callback():
    pass

def stop_video_callback():
    pass

def save_conf_callback():
    global project_directory_var, detection_regions

    if verify_detection_regions():
        detection_regions = get_detection_regions()
        fUtile.set_project_directory(project_directory_var.get())
        fUtile.save_detection_regions(detection_regions)

def get_detection_set(edit_vars):
    return [(edit_vars[0][0].get(), edit_vars[0][1].get()), (edit_vars[1][0].get(), edit_vars[1][1].get())]

def get_detection_regions():
    global M1C_region_vars, M1Cen_region_vars, M1D_region_vars
    global M2C_region_vars, M2Cen_region_vars, M2D_region_vars

    # Update the regions of interest (ROI) for each mouse from the GUI fields
    regions = {
        'm1_c': get_detection_set(M1C_region_vars),
        'm1_cen': get_detection_set(M1Cen_region_vars),
        'm1_d': get_detection_set(M1D_region_vars),
        'm2_c': get_detection_set(M2C_region_vars),
        'm2_cen': get_detection_set(M2Cen_region_vars),
        'm2_d': get_detection_set(M2D_region_vars),
    }
    return regions

def init_detection_set(edit_vars, values):
    for i in range(2):
        for j in range(2):
            edit_vars[i][j].set(values[i][j])

def init_detection_regions():
    global M1C_region_vars, M1Cen_region_vars, M1D_region_vars
    global M2C_region_vars, M2Cen_region_vars, M2D_region_vars

    init_detection_set(M1C_region_vars, detection_regions['m1_c'])
    init_detection_set(M2C_region_vars, detection_regions['m2_c'])
    init_detection_set(M1Cen_region_vars, detection_regions['m1_cen'])
    init_detection_set(M2Cen_region_vars, detection_regions['m2_cen'])
    init_detection_set(M1D_region_vars, detection_regions['m1_d'])
    init_detection_set(M2D_region_vars, detection_regions['m2_d'])

def validate_value(edit_var):
    # region coordinate must be a positive integer
    try:
        num = int(edit_var.get())
    except ValueError:
        num = -1
    if num <= 0 or num > 800:
        messagebox.showerror("Invalid Input", "region coordinate must be positive integer and < 800 ")
        return False
    return True

def verify_detection_set(region_vars):
    data_valid = True
    for i in range(2):
        for j in range(2):
            if not validate_value(region_vars[i][j]):
                data_valid = False

    if data_valid:
        if (region_vars[1][0].get() <= region_vars[0][0].get() or
            region_vars[1][1].get() <= region_vars[0][1].get()):
            messagebox.showerror("Invalid Input", "region must use X2 > X1 and Y2 > Y1")
            data_valid = False
    return data_valid

def verify_detection_regions():
    global M1C_region_vars, M1Cen_region_vars, M1D_region_vars
    global M2C_region_vars, M2Cen_region_vars, M2D_region_vars

    if not verify_detection_set(M1C_region_vars):
        return False
    if not verify_detection_set(M2C_region_vars):
        return False
    if not verify_detection_set(M1Cen_region_vars):
        return False
    if not verify_detection_set(M2Cen_region_vars):
        return False
    if not verify_detection_set(M1D_region_vars):
        return False
    if not verify_detection_set(M2D_region_vars):
        return False
    return True


##############
# main program
##############

window = tk.Tk()
window.title("Prisoner's Dilemma - Detection Regions")
window.geometry("555x595")

# create window layout
system_panel = tk.Frame(window, width=545, height=40, relief=tk.RAISED, borderwidth=2)
system_panel.place(x=5, y=5)
configuration_panel = tk.Frame(window, width=545, height=505, relief=tk.RAISED, borderwidth=2)
configuration_panel.place(x=5, y=50)

# Create entry variables
project_directory_var = tk.StringVar(value=None)
M1C_region_vars = ( (tk.StringVar(value=None), tk.StringVar(value=None)),
                    (tk.StringVar(value=None), tk.StringVar(value=None)) )
M2C_region_vars = ( (tk.StringVar(value=None), tk.StringVar(value=None)),
                    (tk.StringVar(value=None), tk.StringVar(value=None)) )
M1Cen_region_vars = ( (tk.StringVar(value=None), tk.StringVar(value=None)),
                    (tk.StringVar(value=None), tk.StringVar(value=None)) )
M2Cen_region_vars = ( (tk.StringVar(value=None), tk.StringVar(value=None)),
                    (tk.StringVar(value=None), tk.StringVar(value=None)) )
M1D_region_vars = ( (tk.StringVar(value=None), tk.StringVar(value=None)),
                    (tk.StringVar(value=None), tk.StringVar(value=None)) )
M2D_region_vars = ( (tk.StringVar(value=None), tk.StringVar(value=None)),
                    (tk.StringVar(value=None), tk.StringVar(value=None)) )

# Populate Panels
populate_system_parameters_panel(system_panel, project_directory_var)
draw_detection_canvas(configuration_panel, 'M1C', 140, 30, 'n')
draw_detection_canvas(configuration_panel, 'M2C', 320, 30, 'n')
draw_detection_canvas(configuration_panel, 'M1Center', 50, 210, 'w')
draw_detection_canvas(configuration_panel, 'M2Center', 360, 210, 'w')
draw_detection_canvas(configuration_panel, 'M1D', 140, 360, 'n')
draw_detection_canvas(configuration_panel, 'M2D', 320, 360, 'n')

create_detection_set(configuration_panel, M1C_region_vars,140, 30,'n')
create_detection_set(configuration_panel, M2C_region_vars,320, 30,'n')
create_detection_set(configuration_panel, M1Cen_region_vars,50, 210,'w')
create_detection_set(configuration_panel, M2Cen_region_vars,360, 210, 'w')
create_detection_set(configuration_panel, M1D_region_vars, 140, 360, 'n')
create_detection_set(configuration_panel, M2D_region_vars, 320, 360, 'n')

#create buttons
start_video_bt = tk.Button(window, text="Start Video", command=start_video_callback)
start_video_bt.place(x=100, y=560)
stop_video_bt = tk.Button(window, text="Stop Video", command=stop_video_callback)
stop_video_bt.place(x=400, y=560)
save_conf_bt = tk.Button(window, text="Save Regions", command=save_conf_callback)
save_conf_bt.place(x=250, y=560)
save_conf_bt.config(state="disabled")
stop_video_bt.config(state="disabled")

#verify project directory and load regions
pd = fUtile.get_project_directory()
detection_regions = define_regions()
if pd != '':
    project_directory_var.set(pd)
    fUtile.set_project_directory(pd)
    save_conf_bt.config(state="normal")
    tmp = fUtile.load_detection_regions()
    if tmp is not None:
        detection_regions = tmp

init_detection_regions()

window.mainloop()
