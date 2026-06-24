import numpy as np
import cv2
from Video_analyser_code.VideoMouseDetectorABC import VideoMouseDetector

# This class detects presence of a mouse in a region of pixels.
# The basic assumption is that the background is white and the mouse is black.
# It is using CV2's contour detection. A binary black/white mask is applied to the frame.
# the contours are searched for in the masked frame. If more than a minimum number of
# contours are detected in a region, the mouse is there.
# Pixel array is assumed to be monochrome one number per pixel.
# The module does not keep the frames and does not check that the same frame
# size is provided, it's the user's responsibility
# parameters:
#    Binary mask threshold: max pixel value for "Black"

class VideoMouseDetectorCNT(VideoMouseDetector):
    def __init__(self, mask_threshold = 25):
        self.mask_threshold = mask_threshold
        self.contours = None

    def new_frame(self, frame):
        # Define the region (x1, y1, x2, y2)
        x1, y1, x2, y2 = 300, 90, 700, 510

        # Crop the frame to the region of interest
        roi_frame = frame[y1:y2, x1:x2]

        # Apply thresholding on the cropped frame
        ret, thresh = cv2.threshold(roi_frame, self.mask_threshold, 255, cv2.THRESH_BINARY_INV)

        # Find contours in the threshold image
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Adjust the contour coordinates to be relative to the original frame
        self.contours = [contour + np.array([[x1, y1]]) for contour in contours]

    def is_mouse_in_region(self, region=None):
        (x1, y1), (x2, y2) = region
        contour_count = 0
        for contour in self.contours:
            for point in contour:
                x, y = point[0]  # Get the (x, y) coordinates of the contour point
                # print("contour points",point[0])
                if y < 100:
                    tmp = 0
                if x1 <= x <= x2 and y1 <= y <= y2:
                    # Debugging print statement
                    # print(f"Contour Point: {(x, y)}, Region Rect: {region_rect}, Inside: True ,Region key: {region_key}")
                    contour_count +=1
                    break
                else:
                    # Debugging print statement
                    # print(f"Contour Point: {(x, y)}, Region Rect: {region_rect}, Inside: False ,Region key: {region_key}")
                    contour_count = contour_count
        if contour_count > 0:
            contour_count = 1
        return contour_count
