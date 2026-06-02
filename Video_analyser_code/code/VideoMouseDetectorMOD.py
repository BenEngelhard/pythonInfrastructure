import numpy as np
from Video_analyser_code.VideoMouseDetectorABC import VideoMouseDetector

# This class detects presence of a mouse in a region of pixels.
# The basic assumption is that the background is fixed and bright while the mouse is black.
# So the darker the pixels are, its more probable that the mouse is in the region.
# Pixel array is assumed to be monochrome one number per pixel.
# The dark/bright levels are auto calibrated based on average color distribution.
# The most common average color is assumed to be the background. A mouse is detected
# based on deviation towards the dark.
# The module does not keep the frames and does not check that the same frame size
# is provided. It's the user's responsibility
# parameters:
#    bin_number: the resolution of the average color histogram.
#    margin: percentage of the range (mod to 0) that is the detection level
#    hysteresis: percentage difference between mouse in level and mouse out level.

class VideoMouseDetectorMOD(VideoMouseDetector):
    def __init__(self, hysteresis=10, margin=70, bin_number=100, min_frames=200):
        self.frames_color_counts = [0] * bin_number
        self.idle_period = min_frames
        self.hysteresis = hysteresis
        self.margin = margin
        self.mouse_in_region = False
        self.resolution = 255 / bin_number
        self.mod = 0
        self.mod_index = 0
        self.mod_color = 0
        self.current_frame_color = 0

    def new_frame(self, frame):
        self.current_frame_color = np.mean(frame)
        #print (f'Frame color = {frame_color}')
        index = int(self.current_frame_color/self.resolution)
        if index == len(self.frames_color_counts):
            index -= 1  # handle the case of a 255 average frame colore
        self.frames_color_counts[index] += 1
        if self.frames_color_counts[index] > self.mod:
            self.mod = self.frames_color_counts[index]
            self.mod_index = index
            self.mod_color = self.current_frame_color
        if self.idle_period > 0:
            self.idle_period -= 1

    def is_mouse_in_region(self, region=None):
        if not self.idle_period > 0:
            if self.mouse_in_region:
                if self.current_frame_color > self.mod_color * (self.margin + self.hysteresis) / 100:
                    self.mouse_in_region = False
            elif self.current_frame_color < self.mod_color * self.margin / 100:
                    self.mouse_in_region = True
        return self.mouse_in_region
