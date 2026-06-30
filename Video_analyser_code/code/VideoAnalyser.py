#from vmbpy import *
import copy
import time
import cv2
import numpy as np
from queue import Queue
from Video_analyser_code.VideoWriter import VideoWriter
from Video_analyser_code.VideoMouseDetectorAVR import VideoMouseDetectorAVR
from Video_analyser_code.VimbaCameraController import VimbaCameraController
import Data_analysis.FileUtilities as fUtile
import Data_analysis.CodeProfiler as Profiler

def _load_saved_regions():
    saved = fUtile.load_detection_regions()
    if saved is None:
        return None

    if isinstance(saved, dict) and 'region_names' in saved and 'regions' in saved:
        region_names = list(saved['region_names'])
        raw_regions = saved['regions']
    elif isinstance(saved, dict):
        region_names = list(saved.keys())
        raw_regions = saved
    else:
        return None

    regions = {}
    for key in region_names:
        corners = raw_regions[key]
        x1, y1 = int(corners[0][0]), int(corners[0][1])
        x2, y2 = int(corners[1][0]), int(corners[1][1])
        regions[key] = (
            (min(x1, x2), min(y1, y2)),
            (max(x1, x2), max(y1, y2)),
        )
    return regions


class Video_Analyzer:
    def __init__(self, regions=None, region_resolver=None):
        # Initialize the Vimba SDK and VideoAnalyzer
        self.video_file_loc=fUtile.get_file_path(0) + '_video.avi'
        self.video_writer = VideoWriter(output_file=self.video_file_loc)
        self.cam = VimbaCameraController()
        self.region_resolver = region_resolver
        if regions is not None:
            self.regions = regions
            self.region_names = list(regions.keys())
        elif region_resolver is not None:
            self.regions = region_resolver(self.cam)
            self.region_names = list(self.regions.keys())
        else:
            self.regions = self.define_regions()
            self.region_names = list(self.regions.keys())
        #self.pixel_sums = {}
        self.trial_start_time = 0
        self.trial_end_time = None  # Initialize end time
        cv2.namedWindow('MouseCam', cv2.WINDOW_NORMAL)
        self.mouse_detector = [VideoMouseDetectorAVR() for _ in range(len(self.regions))]

    def start_video(self):
        self.trial_start_time = time.time()  # Initialize start time
        self.cam.start_video()

    def define_regions(self):
        saved_regions = _load_saved_regions()
        if saved_regions is not None:
            return saved_regions
        return copy.deepcopy(DEFAULT_DETECTION_REGIONS)

    @staticmethod
    def default_regions():
        return copy.deepcopy(DEFAULT_DETECTION_REGIONS)

    '''
    def find_contours(self, frame):
        # Define the region (x1, y1, x2, y2)
        x1, y1, x2, y2 = 300, 90, 700, 510

        # Crop the frame to the region of interest
        roi_frame = frame[y1:y2, x1:x2]

        # Apply thresholding on the cropped frame
        ret, thresh = cv2.threshold(roi_frame, 25, 255, cv2.THRESH_BINARY_INV)

        # Find contours in the threshold image
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Adjust the contour coordinates to be relative to the original frame
        adjusted_contours = [contour + np.array([[x1, y1]]) for contour in contours]

        return adjusted_contours

    def check_zones(self, frame, mouse_contours):
        zone_activation = [0] * len(self.regions)
        contour_counts = {region_key: 0 for region_key in self.regions}  # Initialize contour counts

        for idx, region_key in enumerate(self.regions):
            (y1, x1), (y2, x2) = self.regions[region_key]
            region_rect = (x1, y1, x2, y2)

            for contour in mouse_contours:
                if self.is_contour_in_region(contour, region_rect, region_key):
                    contour_counts[region_key] += 1  # Increment count for this region

            # Activate zone only if more than 4 contours are detected in the region
            if contour_counts[region_key] > 0:
                zone_activation[idx] = 1

        # Optional: Print the number of contours detected in each region
        #for region_key, count in contour_counts.items():
            #print(f"{region_key}: Number of contours detected = {count}")

        return zone_activation

    def is_contour_in_region(self, contour, region_rect, region_key):
        #x1, y1, w1, h1 = region_rect
        #x2, y2 = x1 + w1, y1 + h1  # Calculate bottom-right corner of the region
        y1,x1, y2, x2 = region_rect
        val=False
        for point in contour:
            x, y = point[0]  # Get the (x, y) coordinates of the contour point
            #print("contour points",point[0])
            if x1 <= x <= x2 and y1 <= y <= y2:
                # Debugging print statement
                #print(f"Contour Point: {(x, y)}, Region Rect: {region_rect}, Inside: True ,Region key: {region_key}")
                val= True
                break
            else:
                # Debugging print statement
                #print(f"Contour Point: {(x, y)}, Region Rect: {region_rect}, Inside: False ,Region key: {region_key}")
                val=False
        return val
    '''

    def format_time(self,seconds):
        # Helper function to format seconds into H:M:S format
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "{:02d}:{:02d}:{:02d}".format(int(h), int(m), int(s))

    def draw_rectangle_with_lines(self, frame, top_left, bottom_right, color, thickness):
        # Unpack the top left and bottom right coordinates
        x1, y1 = top_left
        x2, y2 = bottom_right

        # Draw four lines to form a rectangle
        cv2.line(frame, (x1, y1), (x2, y1), color, thickness)  # Top edge
        cv2.line(frame, (x1, y2), (x2, y2), color, thickness)  # Bottom edge
        cv2.line(frame, (x1, y1), (x1, y2), color, thickness)  # Left edge
        cv2.line(frame, (x2, y1), (x2, y2), color, thickness)  # Right edge

    def draw_regions(self, frame, zone_activations):
        for region_key in self.regions:
            top_left, bottom_right = self.regions[region_key]

            # set region color based on its activation status
            index = list(self.regions.keys()).index(region_key)
            color = 0 if zone_activations[index] == 1 else 255  # black if zone activated white if not
            self.draw_rectangle_with_lines(frame, top_left, bottom_right, color,2)

            # Prepare text for region name
            region_name = region_key
            text = f'{region_name}'

            # Calculate position for the text (slightly inside the top-left corner of the rectangle)
            text_pos = (top_left[0] + 5, top_left[1] + 20)

            # Draw the text
            cv2.putText(frame, text,text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return frame

    def process_single_frame(self):
        zone_activation = [0] * len(self.regions)

        frame = self.cam.get_frame()
        if frame is not None:
            Profiler.NewFrame()
            Profiler.EnterFunction('CV2 Get Image')
            frame_image = frame.as_opencv_image()  # .copy()
            # cam.free_frame(frame)  # return the buffer to the camera controller
            Profiler.ExitFunction('CV2 Get Image')

            for idx, region_key in enumerate(self.regions):
                (x1, y1), (x2, y2) = self.regions[region_key]  # y is vertical dimension on the screen or matrix row
                zone_image = frame_image[y1:y2, x1:x2]

                Profiler.EnterFunction('New Frame')
                self.mouse_detector[idx].new_frame(zone_image)
                Profiler.ExitFunction('New Frame')

                Profiler.EnterFunction('Mouse in Region')
                zone_activation[idx] = self.mouse_detector[idx].is_mouse_in_region()
                Profiler.ExitFunction('Mouse in Region')

            time_since_trial_start = time.time() - self.trial_start_time

            # Format and display trial information and elapsed time
            frame_image = self.draw_regions(frame_image, zone_activation)
            cv2.putText(frame_image, f"Since Start: {self.format_time(time_since_trial_start)}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            Profiler.EnterFunction('Write Frame')
            self.video_writer.write_frame(frame_image)
            Profiler.ExitFunction('Write Frame')

            cv2.imshow('MouseCam', frame_image)
            #cv2.waitKey(1)  # allow imshow() to manage the window. -> Looks like TK is covering for it.
            self.cam.free_frame(frame)   #return the buffer to the camera controller
        else:
            Profiler.IdleLoop()

        return zone_activation

    #def get_zone_activations(self):
        # Return the latest zone activations
        #return self.zone_activations

    def close_resources(self):
        # Close the video writer and any other resources
        self.cam.close_resources()
        self.video_writer.close()
        cv2.destroyAllWindows()

