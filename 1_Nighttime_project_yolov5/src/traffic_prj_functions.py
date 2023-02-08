import math
import cv2
from traffic_prj_constants import *


vehicle_center_points = {}
vehicle_id = 0


# պատկերում է շրջանակ և գրում մեքենայի տեսակը
def display_vehicle_name(x1, y1, x2, y2, confidence, name, color, img):
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
    cv2.putText(img, str(name), (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, COLOR_TEXT, 2)
    cv2.putText(img, str(int(confidence)) + "%", (x1 + 50, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 1, COLOR_TEXT, 1)


# հաշվում է մեքենաների քանակը
def display_vehicles_count(numbers, x2, y2, img):
    numbers += 1
    cv2.line(img, (170, LINE_POSITIONAL1), (1125, LINE_POSITIONAL1), (255, 0, 255), 2)
    cv2.putText(img, str(numbers), (x2, y2), cv2.FONT_HERSHEY_PLAIN, 4, COLOR_TEXT, 4)
    return numbers


def track_vehicles(vehicle_rect):
    global vehicle_id
    vehicles_boxes_ids = []

    # Գտնել նոր մեքենայի կենտրոնի կոորդինատները
    for rect in vehicle_rect:
        index, x, y, w, h = rect
        center_x = x + w / 2
        center_y = y + h / 2

        # Գտնել, արդյոք տվյալ օբյեկտը գտնվել է կրկին
        same_vehicle_detected = False
        for id, pt in vehicle_center_points.items():
            distance = math.hypot(center_x - pt[0], center_y - pt[1])

            if distance < w - x:
                vehicle_center_points[id] = (center_x, center_y)

                vehicles_boxes_ids.append([index, x, y, w, h, id])
                same_vehicle_detected = True
                # break

        # Եթե գտնվել է նոր մեքենա, նրան տալ նոր ID
        if same_vehicle_detected is False:
            vehicle_center_points[vehicle_id] = (center_x, center_y)
            vehicles_boxes_ids.append([index, x, y, w, h, vehicle_id])
            vehicle_id += 1
    return vehicles_boxes_ids
