from VideoAnalyzerSim import Video_Analyzer
from modelling_opponent.MouseMonitor import MouseMonitor
import time


# main code for VideoAnalyzerSim unit test
print("test program for VideoAnalyzerStub")
videoAnalyzer = Video_Analyzer("12")
mouse1 = MouseMonitor(videoAnalyzer, 1)
mouse2 = MouseMonitor(videoAnalyzer, 2)

for i in range(10):
    locations = videoAnalyzer.process_single_frame()
    print(locations)
    print(mouse1.get_mouse_location(locations))
    print(mouse2.get_mouse_location(locations))
    time.sleep(5)

print ("program terminated")