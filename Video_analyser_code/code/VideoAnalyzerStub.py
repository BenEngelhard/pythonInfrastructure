
from locations import Locations

import tkinter as tk



class Video_Analyzer:
    def __init__(self, root):
        self.mouseLocation = [0, 0, 0, 0, 0, 0]  # Initial state with all zeros
        self.root = root
        self.label = tk.Label(self.root, text="Press an arrow key", font=('Helvetica', 16))
        self.label.pack(pady=20)

        # Bind arrow keys to their respective handler functions
        self.root.bind('<Left>', self.left_key)
        self.root.bind('<Right>', self.right_key)
        self.root.bind('<Down>', self.down_key)
        self.root.bind('<Up>', self.up_key)

    def update_label(self):
        self.label.config(text=f"Mouse Location: {self.mouseLocation}")

    def left_key(self, event):
        self.mouseLocation = [0, 0, 1, 0, 0, 0]  # Reset to center state
        self.update_label()

    def right_key(self, event):
        self.mouseLocation = [0, 0, 0, 0, 0, 0]  # Reset to default state
        self.update_label()

    def down_key(self, event):
        self.mouseLocation = [0, 1, 0, 0, 0, 0]  # Set pattern for 'Down'
        self.update_label()

    def up_key(self, event):
        self.mouseLocation = [1, 0, 0, 0, 0, 0]  # Set pattern for 'Up'
        self.update_label()

    def get_mouse_location(self):
        return self.mouseLocation
