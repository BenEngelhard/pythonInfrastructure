# this module simulates the video analyzer. It uses arrow keys to signal mouse locations.
# the mouse location is the last arrow pressed. Mouse 1's location is simulated by the arrow keys
# mouse 2's location is simulated by holding down the left shift key and pressing one of the arrow keys.
from random import random

from pynput.keyboard import Key, Listener
import random

class Video_Analyzer:
    def __init__(self):
        self.mouseLocations = [0] * 6     # a list of 6 zeros
        self.mouse = 1
        self.dropped_frames = 0
        listener = Listener(on_press = self.on_press, on_release = self.on_release)
        listener.start()  # start to listen on a separate thread

    def on_press(self, key):
        if key == Key.shift:
            self.mouse = 2
        if key == Key.left:
            self.updateLocations([1, 0, 0])
        elif key == Key.right:
            self.updateLocations([0, 0, 1])
        elif key == Key.down:
            self.updateLocations([0, 1, 0])
        elif key == Key.up:
            self.updateLocations([0, 0, 0])

    def on_release(self, key):
        if key == Key.shift:
            self.mouse = 1

    def updateLocations(self, locations):
        if self.mouse == 1:
            self.mouseLocations = locations + self.mouseLocations[3:]
        else:
            self.mouseLocations = self.mouseLocations[:3] + locations

    def process_single_frame(self):
        return self.mouseLocations

    def start_video(self):
        pass

    def get_dropped_frames(self):
        frames = random.random()
        if frames > 0.91:
            frames = int(frames * 100) - 90
            print(f'Frames dropped = {frames}')
            self.dropped_frames += frames
        return self.dropped_frames

    def close_resources(self):
        pass