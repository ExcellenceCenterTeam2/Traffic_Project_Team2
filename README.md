# Traffic_Project_Team2

**Show the statistics of the road traffic**

This project is using YOLOv5  Algorithm to perform object recognition and tracking in real time.

**Dependencies**

Python >= 3.8

1. ### Nighttime_project_YOLOv5

**Install the libraries**

*pip install -r requirement.txt*

**Run the code to track and count vehicles with our datasets**

*python3 src/traffic_prj_main.py*


2. ### Daytime_project_YOLOv5

**Run YOLOv5 detection with our datasets**

- from HTTP stream:

*python3 yolov5/detect.py --weights yolov5/runs/train/exp/weights/best.pt  --data datasets/data.yaml --source https://www.youtube.com/watch?v=wqctLW0Hb_0*

- from Video: 

*python3 yolov5/detect.py --weights yolov5/runs/train/exp/weights/best.pt  --data ../datasets/data.yaml --source media/traffic.mp4 --name video_1 --view-img*


3. ### YOLOv5_DeepSort_Pytorch

**Run YOLOv5 DeepSort Tracker with our datasets**

*python3 track_changed.py --source media/test2.mp4 --yolo-weights weights/best.pt  --show-vid --save-vid*








