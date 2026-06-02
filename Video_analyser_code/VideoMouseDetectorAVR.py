import numpy as np
from infrastructure.Video_analyser_code.VideoMouseDetectorABC import VideoMouseDetector

# This class detects presence of a mouse in a region of pixels.
# The basic assumption is that the background is white and the mouse is black.
# So the darker the pixels are, its more probable that the mouse is in the region.
# Pixel array is assumed to be monochrome one number per pixel.
# the dark/bright levels are auto calibrated based on maximum and minimum of the
# moving average.
# the module does not keep the frames and does not check that the same frame size
# is provided. It's the user's responsibility
# parameters:
#    buffer_depth: how many frames are averaged
#    margin: percentage of the range (average max-min) that is the detection level
#    hysteresis: percentage difference between mouse in level and mouse out level.
#    min_range: the min difference between min and max frame average that will enable detection

class VideoMouseDetectorAVR(VideoMouseDetector):
    def __init__(self, hysteresis=10, margin=30, buffer_depth=10, min_range=50):
        self.frames_color_buffer = [0] * buffer_depth
        self.frames_pointer = 0
        self.first_wrap = True
        self.frames_min = float('inf')
        self.frames_max = 0
        self.frames_sum = 0
        self.frames_average = 0
        self.hysteresis = hysteresis
        self.margin = margin
        self.mouse_in_region = False
        self.min_range = min_range

    def new_frame(self, frame):
        average_frame_color = np.mean(frame)
        #print (f'Frame color = {frame_color}')
        self.frames_sum -= self.frames_color_buffer[self.frames_pointer]
        self.frames_color_buffer[self.frames_pointer] = average_frame_color
        self.frames_sum += self.frames_color_buffer[self.frames_pointer]
        self.frames_pointer += 1
        if self.frames_pointer == len(self.frames_color_buffer):
            self.frames_pointer = 0
            self.first_wrap = False
        if not self.first_wrap:
            self.frames_average = self.frames_sum / len(self.frames_color_buffer)
            if self.frames_average < self.frames_min:
                self.frames_min = self.frames_average
                #print(f'minimum frames average: {self.frames_min}')
            if self.frames_average > self.frames_max:
                self.frames_max = self.frames_average
                #print(f'maximum frames average: {self.frames_max}')

    def is_mouse_in_region(self, region=None):
        if not self.first_wrap: # no detection is attempted before the frame buffer is filled at least once.
            average_range = self.frames_max - self.frames_min
            if average_range > self.min_range:
                if self.mouse_in_region:
                    if self.frames_average > self.frames_min + average_range * (self.margin + self.hysteresis) / 100:
                        self.mouse_in_region = False
                elif self.frames_average < self.frames_min + average_range * self.margin / 100:
                        self.mouse_in_region = True
        return self.mouse_in_region


