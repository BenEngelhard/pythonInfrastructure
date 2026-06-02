import time
import cv2
import tkinter as tk

from infrastructure.Video_analyser_code.VideoMouseDetectorMOD import VideoMouseDetectorMOD
from infrastructure.Video_analyser_code.VideoMouseDetectorAVR import VideoMouseDetectorAVR
from infrastructure.Video_analyser_code.VideoMouseDetectorCNT import VideoMouseDetectorCNT
from infrastructure.Video_analyser_code.VimbaCameraController import (VimbaCameraController)
import infrastructure.Data_analysis.CodeProfiler as Profiler


def define_regions():
    # Define the regions of interest (ROI) for each mouse and their specific zones
    regions = {
        'm1_c': [(485, 145), (515, 215)],  # Mouse 2 Cooperate Zone (Top Left)
        'm1_cen': [(355, 290), (410, 335)],  # Mouse 2 Center Zone (Center Left)
        'm1_d': [(485, 410), (515, 480)],  # Mouse 2 Defect Zone (Bottom Left)
        'm2_c': [(540, 145), (570, 215)],  # Mouse 1 Cooperate Zone (Top Right)
        'm2_cen': [(635, 290), (690, 335)],  # Mouse 1 Center Zone (Center Right)
        'm2_d': [(540, 410), (570, 480)],  # Adjusted Mouse 1 Defect Zone (Bottom Right)
    }
    return regions

def draw_rectangle_with_lines(frame, top_left, bottom_right, color, thickness):
    # Unpack the top left and bottom right coordinates
    x1, y1 = top_left
    x2, y2 = bottom_right

    # Draw four lines to form a rectangle
    cv2.line(frame, (x1, y1), (x2, y1), color, thickness)  # Top edge
    cv2.line(frame, (x1, y2), (x2, y2), color, thickness)  # Bottom edge
    cv2.line(frame, (x1, y1), (x1, y2), color, thickness)  # Left edge
    cv2.line(frame, (x2, y1), (x2, y2), color, thickness)  # Right edge

def draw_regions(frame_image, zone_activations):
    for region_key in regions:
        top_left, bottom_right = regions[region_key]

        # set region color based on its activation status
        index = list(regions.keys()).index(region_key)
        color = 0 if zone_activations[index] == 1 else 255  # black if zone activated white if not
        draw_rectangle_with_lines(frame_image, top_left, bottom_right, color, 2)

        # Prepare text for region name
        region_name = region_key
        text = f'{region_name}'

        # Calculate position for the text (slightly inside the top-left corner of the rectangle)
        text_pos = (top_left[0] + 5, top_left[1] + 20)

        # Draw the text
        cv2.putText(frame_image, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    return frame_image

def stop_test():
    global window
    window.destroy()

def start_test():
    global cam

    cv2.namedWindow('MouseCam', cv2.WINDOW_NORMAL)
    cam.start_video()
    start_button.after(1, timer_event)

def algorithm_1_detection(frame_image):
    for idx, region_key in enumerate(regions):
        (x1, y1), (x2, y2) = regions[region_key]  # y is vertical dimension on the screen or matrix row
        zone_image = frame_image[y1:y2, x1:x2]

        Profiler.EnterFunction('New Frame')
        mouse_detector[idx].new_frame(zone_image)
        Profiler.ExitFunction('New Frame')

        Profiler.EnterFunction('Mouse in Region')
        zone_activation[idx] = mouse_detector[idx].is_mouse_in_region()
        Profiler.ExitFunction('Mouse in Region')

def algorithm_2_detection(frame_image):
    Profiler.EnterFunction('New Frame')
    mouse_detector.new_frame(frame_image)
    Profiler.ExitFunction('New Frame')

    for idx, region_key in enumerate(regions):
        Profiler.EnterFunction('Mouse in Region')
        zone_activation[idx] = mouse_detector.is_mouse_in_region(regions[region_key])
        if zone_activation[0] == 1:
            tmp = 0
        Profiler.ExitFunction('Mouse in Region')

def timer_event():
    global cam
    global mouse_detector
    global regions
    global zone_activation

    frame = cam.get_frame()
    if frame is not None:
        Profiler.NewFrame()
        Profiler.EnterFunction('Frame Handling')
        Profiler.EnterFunction('CV2 Get Image')
        frame_image = frame.as_opencv_image() #.copy()
        #cam.free_frame(frame)  # return the buffer to the camera controller
        Profiler.ExitFunction('CV2 Get Image')

        Profiler.EnterFunction('Region Handling')
        if algorithm == 1 or algorithm == 3:
            algorithm_1_detection(frame_image)
        elif algorithm == 2:
            algorithm_2_detection(frame_image)
        else:
            print('Algorithm definition error')
            exit()
        Profiler.ExitFunction('Region Handling')

        Profiler.EnterFunction('Draw Image')
        frame_image = draw_regions(frame_image, zone_activation)
        Profiler.ExitFunction('Draw Image')

        Profiler.EnterFunction('Image Show')
        cv2.imshow('MouseCam', frame_image)
        Profiler.ExitFunction('Image Show')
        #cv2.waitKey(1)  # allow imshow() to manage the window. -> looks like TK is covering for it
        cam.free_frame(frame)  # return the buffer to the camera controller
        Profiler.ExitFunction('Frame Handling')
    else:
        Profiler.IdleLoop()

    start_button.after(1, timer_event)

# main program level
algorithm = 3     # 1 - frame average color, 2 - contour detection, 3 - frame mod color
cam = VimbaCameraController()
regions = define_regions()
zone_activation = [0] * 6
end_test = False
start_time = time.time()
if algorithm == 1:
    mouse_detector = [VideoMouseDetectorAVR() for _ in range(len(zone_activation))]
elif algorithm == 2:
    mouse_detector = VideoMouseDetectorCNT()
elif algorithm == 3:
    mouse_detector = [VideoMouseDetectorMOD() for _ in range(len(zone_activation))]
else:
    print('Algorithm definition error')
    exit()

window = tk.Tk()
window.title('Mouse detection test')
window.geometry("300x70")

start_button = tk.Button(window, text="Start Test", command=start_test)
start_button.place(x=50, y=10)
stop_button = tk.Button(window, text="Stop Test", command=stop_test)
stop_button.place(x=150, y=10)

window.mainloop()

# close and release
cam.close_resources()
cv2.destroyAllWindows()
