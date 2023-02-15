import cv2
import numpy as np
from traffic_prj_functions import *
from traffic_prj_constants import *


frame_count = 0
number_of_cars_leaving = 0
number_of_trucks_leaving = 0
number_of_cars_entering = 0
number_of_trucks_entering = 0
start_frame_time = time.time()

def process_frames(cap):
    while True:
        ret, img = cap.read()
        if not ret:
            break
        global frame_count, number_of_cars_leaving, number_of_trucks_leaving, number_of_cars_entering, number_of_trucks_entering
        frame_count += 1
        if frame_count % 4 != 0:
            continue
        fps = calculate_fps(start_frame_time, frame_count)
        cv2.putText(img, "FPS : " + str(int(fps)), (50, 1000), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        height, width, _ = img.shape
        new_width = 1280
        new_height = int((new_width/width)*height)
        img = cv2.resize(img, (new_width, new_height))
        cv2.line(img, (695, LINE_POSITIONAL1), (1125, LINE_POSITIONAL1), COLOR_LINE, 3)
        cv2.line(img, (170, LINE_POSITIONAL1), (600, LINE_POSITIONAL1), COLOR_LINE, 3)
        results = model(img, 416)
        detection = []
        vehicle_obj = track_vehicles(detection)
        for row in vehicle_obj:
            x1, y1, x2, y2, id = row
            detection.append([x1, y1, x2, y2])
        for row in results.xyxy[0]:
            x1, y1, x2, y2, conf, vehicle_class = row
            print(row)
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
            vehicle_confidence = conf * 100

            if vehicle_class == 0:
                display_vehicle_name(x1, y1, x2, y2, vehicle_confidence, CAR, COLOR_CAR, img)
            if vehicle_class == 1:
                display_vehicle_name(x1, y1, x2, y2, vehicle_confidence, TRUCK, COLOR_TRUCK, img)

            center_x, center_y = int((x1 + x2) / 2), int((y1 + y2) / 2)
            cv2.circle(img, (center_x, center_y), 4, (0, 255, 0), -1)

            if center_y < (LINE_POSITIONAL2 + OFFSET1 ) and center_y > (LINE_POSITIONAL2 - OFFSET1-2) and center_x < 650:
                if vehicle_class == 0:
                    number_of_cars_leaving = display_vehicles_count(number_of_cars_leaving, x2, y2, img)
                if vehicle_class == 1:
                    number_of_trucks_leaving = display_vehicles_count(number_of_trucks_leaving, x2, y2, img)
            if center_y < (LINE_POSITIONAL1 + OFFSET2-4) and center_y > (LINE_POSITIONAL1 - OFFSET2-2) and center_x > 650:
                if vehicle_class == 0:
                    number_of_cars_entering = display_vehicles_count(number_of_cars_entering, x2, y2, img)
                if vehicle_class == 1:
                    number_of_trucks_entering = display_vehicles_count(number_of_trucks_entering, x2, y2, img)

        cv2.putText(img, "Number of Cars Leaving: " + str(number_of_cars_leaving), (35, 35), cv2.FONT_HERSHEY_PLAIN, 2, COLOR_TEXT, 2)
        cv2.putText(img, "Number of Trucks Leaving: " + str(number_of_trucks_leaving), (35, 70), cv2.FONT_HERSHEY_PLAIN, 1.85, COLOR_TEXT, 2)
        cv2.putText(img, "Number of Cars Entering: " + str(number_of_cars_entering), (740, 35), cv2.FONT_HERSHEY_PLAIN, 2, COLOR_TEXT, 2 )
        cv2.putText(img, "Number of Trucks Entering: " + str(number_of_trucks_entering), (740, 70), cv2.FONT_HERSHEY_PLAIN, 1.85, COLOR_TEXT, 2)

        cv2.imshow("IMG", img)
        if cv2.waitKey(20) & 0xFF == ord("q"):
            break


cap = cv2.VideoCapture("media/test1.mp4")
process_frames(cap)
cap.release()
cv2.destroyAllWindows()


    
