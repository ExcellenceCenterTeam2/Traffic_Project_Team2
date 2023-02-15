import numpy as np
import torch
import cv2


cap=cv2.VideoCapture("media/traffic.mp4")
result = cv2.VideoWriter('test1.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, (700, 500))

path='yolov5/runs/train/exp/weights/best.pt'


model = torch.hub.load('yolov5', 'custom', path,source='local')

c=model.names[0] = 'car'
l=model.names[1] = 'lorry'



size=416

count=0
counter=0


color=(0,0,255)

cy1=360
offset=20
while True:
    ret,img=cap.read()

    count += 1
    if count % 4 != 0:
        continue
    img=cv2.resize(img,(700,500))
    #cv2.line(img,(79, cy1), (699, cy1), (255,0,0),2) #tvid.mp4
    cv2.line(img,(0, cy1), (699, cy1), (255,0,0),2)
    results=model(img,size)
    a = results.pandas().xyxy[0]
    for index, row in results.pandas().xyxy[0].iterrows():
        print(row)
        x1 = int(row['xmin'])
        y1 = int(row['ymin'])
        x2 = int(row['xmax'])
        y2 = int(row['ymax'])
        d = (row['class'])
        if d==0:
            cv2.rectangle(img, (x1,y1), (x2,y2), (0, 0, 255), 1)
            cv2.putText(img, str(c), (x1, y1-10), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0),1)
        if d==1:
            cv2.rectangle(img, (x1,y1), (x2,y2), (0, 254, 255), 1)
            cv2.putText(img, str(l), (x1, y1), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255),1)
        rectx1, recty1 = ((x1+x2)/2, (y1+y2)/2)
        rect_center = int(rectx1), int(recty1)
            #print(rect_center)
        cx = rect_center[0]
        cy = rect_center[1]
        cv2.circle(img, (cx, cy), 1, (0, 255, 0), -1)
        if cy < (cy1+offset) and cy > (cy1-offset) and cx > 400:
            counter+=1
            cv2.line(img,(0, cy1), (699, cy1), (255,0,255),2)
            print("c=",counter)
            cv2.putText(img, str(counter), (x2, y2), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255),4)
    cv2.putText(img, "Total Cars entering: " +str(counter), (257, 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    result.write(img)
    cv2.imshow("IMG",img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
result.release()
cv2.destroyAllWindows()
