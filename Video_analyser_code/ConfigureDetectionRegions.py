import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import ctypes
import infrastructure.Data_analysis.FileUtilities as fUtile
from infrastructure.Video_analyser_code.VimbaCameraController import VimbaCameraController


class ConfigureDetectionRegions:
    def __init__(self, roi_name_list):
        ctypes.windll.shcore.SetProcessDpiAwareness(1) # disable window scaling
        self.window = tk.Tk()
        self.window.title("Mouse Detection Regions")
        self.window.geometry("978x760")
        self.window.focus_set()
        self.canvas_rects = {name: [] for name in roi_name_list}
        self.canvas_texts = {name: [] for name in roi_name_list}
        # screen_width = window.winfo_screenwidth()    # future feature
        # screen_height = window.winfo_screenheight()
        self.cam = VimbaCameraController(50)
        self.cam.start_video()
        self.project_directory_var = None
        self.save_conf_bt = None
        self.video_canvas = None
        self.img_id = None
        self.roi_start_x = self.roi_start_y = 0  # ROI control variables
        self.roi_names_combo = None
        self.selected_roi = ''
        self.calibrate_bt = None
        self.save_conf_bt = None
        self.gui_layout()
        self.bind_gui_event()

    def populate_system_parameters_panel(self, panel, pdVar):
        tk.Label(panel, text="Project Directory:").place(x=5, y=10)
        pd_name_entry = tk.Entry(panel, width=70, textvariable=pdVar)
        pd_name_entry.place(x=150, y=10)
        pd_button = tk.Button(panel, text="Browse", command=self.browse_project_directory)
        pd_button.place(x=875, y=5)

    def browse_project_directory(self):
        directory_path = filedialog.askdirectory(title="Select a directory")
        if directory_path != "":
            self.project_directory_var.set(directory_path)
            self.save_conf_bt.config(state="normal")

    def save_conf_callback(self):
        detection_regions = {}
        missing_region = False
        for name in self.canvas_rects:
            rect_id = self.canvas_rects.get(name)
            if rect_id:
                x0, y0, x1, y1 = self.video_canvas.coords(rect_id)
                x0, x1 = sorted((x0, x1))
                y0, y1 = sorted((y0, y1))
                detection_regions[name] = [int(x0), int(y0), int(x1), int(y1)]
            else:
                missing_region = True
                messagebox.showerror("Error", f'{name} is undefined')
                break
        if not missing_region:
            fUtile.set_project_directory(self.project_directory_var.get())
            fUtile.save_detection_regions(detection_regions)

    def update_video_frame(self):
        frame = self.cam.get_frame()
        if frame is not None:
            frame_image = frame.as_opencv_image()
            frame_rgb = cv2.cvtColor(frame_image, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(img_pil)
            self.video_canvas.img = img_tk
            self.video_canvas.itemconfig(self.img_id, image=img_tk)
            self.cam.free_frame(frame)  # return the buffer to the camera controller
        self.window.after(1, self.update_video_frame)

    # Mouse event handlers
    def start_roi(self, event):   # mouse button pressed on canvas
        if self.selected_roi != '':
            self.roi_start_x = event.x
            self.roi_start_y = event.y

    def update_roi(self, event):   # mouse move, button pressed
        if self.selected_roi != '':
            rect_id = self.canvas_rects.get(self.selected_roi)
            if not rect_id:
                self.canvas_rects[self.selected_roi] = self.video_canvas.create_rectangle(self.roi_start_x, self.roi_start_y,
                                                               event.x, event.y, outline="red", width=2)
                self.canvas_texts[self.selected_roi] = self.video_canvas.create_text(self.roi_start_x, self.roi_start_y - 5,
                                                                text=self.selected_roi, font=("Arial", 12), anchor="sw", fill="red")
            else:
                self.video_canvas.coords(rect_id, self.roi_start_x, self.roi_start_y, event.x, event.y)
                text_id = self.canvas_texts.get(self.selected_roi)
                self.video_canvas.coords(text_id, self.roi_start_x, self.roi_start_y)

    def end_roi(self, event):  # mouse button released
        if self.selected_roi != '':
            # Compute ROI coordinates in canvas/video frame coordinates
            x0 = min(self.roi_start_x, event.x)
            y0 = min(self.roi_start_y, event.y)
            x1 = max(self.roi_start_x, event.x)
            y1 = max(self.roi_start_y, event.y)
            print(f"ROI coordinates: ({x0}, {y0}) -> ({x1}, {y1})")

    # Keyboard event handlers
    def on_up(self, event):
        if self.selected_roi != '':
            rect_id = self.canvas_rects.get(self.selected_roi)
            if rect_id:
                x0, y0, x1, y1 = self.video_canvas.coords(rect_id)
                x0, x1 = sorted((x0, x1))
                y0, y1 = sorted((y0, y1))
                if event.state & 0x0001:    # Shift pressed -> move up
                    y0 = y0 - 1
                    y1 = y1 - 1
                else:                       # increase vertically
                    y0 = y0 - 1
                    y1 = y1 + 1
                self.video_canvas.coords(rect_id, x0, y0, x1, y1)

    def on_down(self, event):
        if self.selected_roi != '':
            rect_id = self.canvas_rects.get(self.selected_roi)
            if rect_id:
                x0, y0, x1, y1 = self.video_canvas.coords(rect_id)
                x0, x1 = sorted((x0, x1))
                y0, y1 = sorted((y0, y1))
                if event.state & 0x0001:  # Shift pressed -> move down
                    y0 = y0 + 1
                    y1 = y1 + 1
                else:                       # decrease vertically
                    y0 = y0 + 1
                    y1 = y1 - 1
                self.video_canvas.coords(rect_id, x0, y0, x1, y1)

    def on_left(self, event):
        if self.selected_roi != '':
            rect_id = self.canvas_rects.get(self.selected_roi)
            if rect_id:
                x0, y0, x1, y1 = self.video_canvas.coords(rect_id)
                x0, x1 = sorted((x0, x1))
                y0, y1 = sorted((y0, y1))
                if event.state & 0x0001:  # Shift pressed -> move left
                    x0 = x0 - 1
                    x1 = x1 - 1
                else:                     # dec crease horizontally
                    x0 = x0 + 1
                    x1 = x1 - 1
                self.video_canvas.coords(rect_id, x0, y0, x1, y1)

    def on_right(self, event):
        if self.selected_roi != '':
            rect_id = self.canvas_rects.get(self.selected_roi)
            if rect_id:
                x0, y0, x1, y1 = self.video_canvas.coords(rect_id)
                x0, x1 = sorted((x0, x1))
                y0, y1 = sorted((y0, y1))
                if event.state & 0x0001:  # Shift pressed -> move right
                    x0 = x0 + 1
                    x1 = x1 + 1
                else:                       # increase horizontally
                    x0 = x0 - 1
                    x1 = x1 + 1
                self.video_canvas.coords(rect_id, x0, y0, x1, y1)

    def gui_layout(self):
        # create window layout
        system_panel = tk.Frame(self.window, width=968, height=60, relief=tk.RAISED, borderwidth=2)
        system_panel.place(x=5, y=5)

        self.video_canvas = tk.Canvas(self.window, width=968, height=608)
        self.video_canvas.place(x=5, y=70)
        self.img_id = self.video_canvas.create_image(0, 0, anchor="nw")

        control_panel = tk.Frame(self.window, width=968, height=60, relief=tk.RAISED, borderwidth=2)
        control_panel.place(x=5, y=690)

        # Create entry variables
        self.project_directory_var = tk.StringVar(value=None)

        # Populate Panels
        self.populate_system_parameters_panel(system_panel, self.project_directory_var)

        #create buttons
        self.save_conf_bt = tk.Button(control_panel, text="Save", command=self.save_conf_callback)
        self.save_conf_bt.place(x=770, y=5)
        self.save_conf_bt.config(state="disabled")
        self.roi_names_combo = ttk.Combobox(control_panel,values=list(self.canvas_rects.keys()))
        self.roi_names_combo.place(x=500, y=15)
        self.roi_names_combo.bind("<<ComboboxSelected>>", self.on_combo_selected)

        self.update_video_frame()

    def on_combo_selected(self, event):
        self.selected_roi = self.roi_names_combo.get()

        for name in self.canvas_rects:
            rect_id = self.canvas_rects.get(name)
            text_id = self.canvas_texts.get(name)
            if rect_id is not None: # rect is defined
                if name == self.selected_roi:
                    self.video_canvas.itemconfig(rect_id, outline="red")
                    self.video_canvas.itemconfig(text_id, fill="red")
                else:
                    self.video_canvas.itemconfig(rect_id, outline="white")
                    self.video_canvas.itemconfig(text_id, fill="white")
        self.window.focus_set()

    def bind_gui_event(self):
        # Bind mouse and keyboard event handlers
        self.video_canvas.bind("<Button-1>", self.start_roi)  # left mouse button pressed
        self.video_canvas.bind("<B1-Motion>", self.update_roi)  # mouse dragged with button 1
        self.video_canvas.bind("<ButtonRelease-1>", self.end_roi)  # left mouse button released
        self.window.bind("<Up>", self.on_up)
        self.window.bind("<Down>", self.on_down)
        self.window.bind("<Left>", self.on_left)
        self.window.bind("<Right>", self.on_right)

    def configure(self):
        # verify project directory and load regions
        pd = fUtile.get_project_directory()
        if pd != '':
            self.project_directory_var.set(pd)
            fUtile.set_project_directory(pd)
            det_regions = fUtile.load_detection_regions()
            if det_regions is not None:
                for name in det_regions:
                    x0, y0, x1, y1 = det_regions[name]
                    self.canvas_rects[name] = self.video_canvas.create_rectangle(x0, y0, x1, y1, outline="white", width=2)
                    self.canvas_texts[name] = self.video_canvas.create_text(x0, y0 - 5, text=name, font=("Arial", 12), anchor="sw", fill="white")
                    self.save_conf_bt.config(state="normal")
            else:
                answer = messagebox.askyesno("Confirm", "Detection regions file does not exist. Initialize?")
                if answer:
                    self.save_conf_bt.config(state="normal")
        self.window.mainloop()
