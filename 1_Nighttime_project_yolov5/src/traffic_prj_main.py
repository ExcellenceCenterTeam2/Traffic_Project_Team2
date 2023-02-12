import cv2
import time
from traffic_prj_functions import *
from traffic_prj_constants import *


#fps = 30
frame_count = 0
number_of_cars_leaving = 0
number_of_trucks_leaving = 0
number_of_cars_entering = 0
number_of_trucks_entering = 0


#def frame_per_second():
 #   global fps, start_frame_time, current_frame_time, frame_count
  #  elapsed_time = current_frame_time - start_frame_time
   # if elapsed_time > 1:
    #    fps = frame_count / elapsed_time
     #   frame_count = 0
      #  start_frame_time = current_frame_time
    #return fps


cap = cv2.VideoCapture("media/test1.mp4")
start_frame_time = time.time()
while True:
    ret, img = cap.read()
    frame_count += 1
    if frame_count % 4 != 0:
        continue
    # fps = cap.get(cv2.CAP_PROP_FPS)
    current_frame_time = time.time()
    fps = calculate_fps(start_frame_time, frame_count)
    cv2.putText(img, "FPS : " + str(int(fps)), (50, 1000), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

    img = cv2.resize(img, (1280, 720))
    cv2.line(img, (695, LINE_POSITIONAL1), (1125, LINE_POSITIONAL1), COLOR_LINE, 3)
    cv2.line(img, (170, LINE_POSITIONAL1), (600, LINE_POSITIONAL1), COLOR_LINE, 3)

    results = model(img, 200)
    detection = []
    for index, row in results.pandas().xyxy[0].iterrows():
        print(row)
        x1 = int(row["xmin"])
        y1 = int(row["ymin"])
        x2 = int(row["xmax"])
        y2 = int(row["ymax"])
        vehicle_class = row["class"]
        vehicle_confidence = (row["confidence"]) * 100

        if vehicle_class == 0:
            display_vehicle_name(x1, y1, x2, y2, vehicle_confidence, CAR, COLOR_CAR, img)
        if vehicle_class == 1:
            display_vehicle_name(x1, y1, x2, y2, vehicle_confidence, TRUCK, COLOR_TRUCK, img)

        center_x, center_y = int((x1 + x2) / 2), int((y1 + y2) / 2)
        cv2.circle(img, (center_x, center_y), 4, (0, 255, 0), -1)

        detection.append([index, x1, y1, x2, y2])
        vehicle_obj = track_vehicles(detection)
        for row in vehicle_obj:
            index, x1, y1, x2, y2, id = row

        if center_y < (LINE_POSITIONAL2 + OFFSET1 + 4) and center_y > (LINE_POSITIONAL2 - OFFSET1) and center_x < 650:
            if vehicle_class == 0:
                number_of_cars_leaving = display_vehicles_count(number_of_cars_leaving, x2, y2, img)
            if vehicle_class == 1:
                number_of_trucks_leaving = display_vehicles_count(number_of_trucks_leaving, x2, y2, img)
        if center_y < (LINE_POSITIONAL1 + OFFSET2) and center_y > (LINE_POSITIONAL1 - OFFSET2) and center_x > 650:
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
    
cap.release()
cv2.destroyAllWindows()
