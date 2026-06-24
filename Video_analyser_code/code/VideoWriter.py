from vidgear.gears import WriteGear
import time


class VideoWriter:
    def __init__(self, output_file, frame_size=(968, 608), fps=30.0):
        self.output_file = output_file
        self.frame_size = frame_size
        self.fps = fps
        self.writer = WriteGear(output=self.output_file)
        self.frame_time = 1/50
        self.time_to_next_frame = 0

    def write_frame(self, frame):
        if self.time_to_next_frame == 0:
            self.time_to_next_frame = time.time() + self.frame_time
            self.writer.write(frame)
        else:
            #print(time.time(), self.time_to_next_frame, self.frame_time)
            while time.time() > self.time_to_next_frame:
                self.writer.write(frame)
                self.time_to_next_frame += self.frame_time

    def close(self):
        self.writer.close()
