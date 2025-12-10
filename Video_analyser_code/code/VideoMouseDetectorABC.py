from abc import ABC, abstractmethod

class VideoMouseDetector (ABC):

    @abstractmethod
    def new_frame(self, frame):
        pass

    @abstractmethod
    def is_mouse_in_region(self, region=None):
        pass

