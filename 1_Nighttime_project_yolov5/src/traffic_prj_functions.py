import math
import cv2
from traffic_prj_constants import *


vehicle_center_points = {}
vehicle_id = 0


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
	Track vehicles in a video by assigning unique IDs to each vehicle.
	This function takes in the `vehicle_rect` which is a list of rectangles representing the
	detected vehicles in a frame. It then checks if the vehicle has been detected previously
	by finding its center coordinates and comparing it to the stored vehicle center points.
	If a match is found, the same ID is assigned to the vehicle, otherwise a new ID is
	assigned to the new vehicle.
	Parameters:
	- vehicle_rect (list): A list of rectangles representing the detected vehicles in a frame.
    	Each rectangle is represented as a list with 6 values: [index, x, y, w, h, id].
    	The index is the index of the vehicle in the `vehicle_rect` list, x and y are the
    	coordinates of the top-left point of the rectangle, w and h are the width and height
    	of the rectangle and id is the assigned ID of the vehicle.
	Returns:
	- vehicles_boxes_ids (list): A list of rectangles with assigned IDs representing the
    	detected vehicles in a frame.
	"""
    global vehicle_id
    vehicles_boxes_ids = []

    for rect in vehicle_rect:
        index, x, y, w, h = rect
        center_x = x + w / 2
        center_y = y + h / 2

        same_vehicle_detected = False
        for id, pt in vehicle_center_points.items():
            distance = math.hypot(center_x - pt[0], center_y - pt[1])

            if distance < w - x:
                vehicle_center_points[id] = (center_x, center_y)

                vehicles_boxes_ids.append([index, x, y, w, h, id])
                same_vehicle_detected = True
                # break

        if same_vehicle_detected is False:
            vehicle_center_points[vehicle_id] = (center_x, center_y)
            vehicles_boxes_ids.append([index, x, y, w, h, vehicle_id])
            vehicle_id += 1
    return vehicles_boxes_ids
