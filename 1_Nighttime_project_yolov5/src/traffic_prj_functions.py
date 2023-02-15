import math
import time
import cv2
from traffic_prj_constants import *


vehicle_center_points = {}
vehicle_id = 0

def calculate_fps(start_time, frame_count):
    """
    Calculates the frames per second (FPS) given the start time and the total number of frames processed.

    Parameters:
    start_time (float): The start time of the video processing, in seconds (obtained using `time.time()`).
    frame_count (int): The total number of frames processed.

    Returns:
    float: The calculated frames per second.

    """
    return frame_count / (time.time() - start_time)

def display_vehicle_name(x1, y1, x2, y2, confidence, name, color, img):
    """
	Display the name and confidence of a detected vehicle in an image.

	Parameters:
	x1 (int): x coordinate of the top-left corner of the bounding box
	y1 (int): y coordinate of the top-left corner of the bounding box
	x2 (int): x coordinate of the bottom-right corner of the bounding box
	y2 (int): y coordinate of the bottom-right corner of the bounding box
	confidence (float): confidence score of the detection
	name (str): name of the detected vehicle
	color (tuple): RGB color code to use for the bounding box and text
	img (ndarray): original image, to display the bounding box and text on

	Returns:
	None
	"""

    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
    cv2.putText(img, str(name), (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, COLOR_TEXT, 2)
    cv2.putText(img, str(int(confidence)) + "%", (x1 + 50, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 1, COLOR_TEXT, 1)


def display_vehicles_count(numbers, x2, y2, img):
    """
	Display the count of detected vehicles in an image.

	Parameters:
	numbers (int): current count of detected vehicles
	x2 (int): x coordinate to display the count at
	y2 (int): y coordinate to display the count at
	img (ndarray): original image, to display the count on

	Returns:
	int: updated count of detected vehicles
	"""
    numbers += 1
    cv2.line(img, (170, LINE_POSITIONAL1), (1125, LINE_POSITIONAL1), (255, 0, 255), 2)
    cv2.putText(img, str(numbers), (x2, y2), cv2.FONT_HERSHEY_PLAIN, 4, COLOR_TEXT, 4)
    return numbers


def track_vehicles(vehicle_rect):
    """
    Given a list of vehicle bounding boxes in the form [index, x_min, y_min, x_max, y_max],
    this function tracks the detected vehicles over time, assigns a unique ID to each vehicle,
    and returns a list of bounding boxes with their corresponding vehicle IDs.
    Parameters:
    vehicle_rect : list
        A list of vehicle bounding boxes, where each bounding box is a list of
        [index, x_min, y_min, x_max, y_max] that represents the index of the frame,
        and the coordinates of the top-left and bottom-right corners of the bounding box.
    Returns:
    vehicles_boxes_ids : list
        A list of vehicle bounding boxes, where each bounding box is a list of
        [index, x_min, y_min, x_max, y_max, id], that represents the index of the frame,
        the coordinates of the top-left and bottom-right corners of the bounding box,
        and the ID of the vehicle that the bounding box corresponds to.
    """
    global vehicle_id
    vehicles_boxes_ids = []

    for rect in vehicle_rect:
        index, x_min, y_min, x_max, y_max = rect
        center_x = int((x_min + x_max) / 2)
        center_y = int((y_min + y_max) / 2)

        same_vehicle_detected = False
        for id, pt in vehicle_center_points.items():
            distance = math.hypot(center_x - pt[0], center_y - pt[1])
            width = x_max-x_min
            if distance < width/2:
                vehicle_center_points[id] = (center_x, center_y)

                vehicles_boxes_ids.append([index, x_min, y_min, x_max, y_max, id])
                same_vehicle_detected = True
                # break

        if same_vehicle_detected is False:
            vehicle_center_points[vehicle_id] = (center_x, center_y)
            vehicles_boxes_ids.append([index, x_min, y_min, x_max, y_max, vehicle_id])
            vehicle_id += 1
    return vehicles_boxes_ids
