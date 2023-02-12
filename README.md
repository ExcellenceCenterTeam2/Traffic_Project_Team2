# Traffic_Project_Team2

**Show the statistics of the road traffic**

This project is using YOLOv5  Algorithm to perform object recognition and tracking in real time.

**Dependencies**

Python >= 3.8

**Install the libraries**

*pip install -r requirement.txt*

1. ### Nighttime_project_YOLOv5


**Run the code to track and count vehicles with our datasets**

*python3 src/traffic_prj_main.py*

***directories to project Nighttime_project_yolov5***

 - datasets
 - media: download the folder media from google drive 
 
 link: https://drive.google.com/drive/folders/1FHLs04jdQPBuSbD4Yh8LCdpDKi5nwhlA?usp=sharing
 - src
 - yolov5

2. ### Daytime_project_YOLOv5

**Run YOLOv5 detection with our datasets**

- from HTTP stream:

*python3 yolov5/detect.py --weights yolov5/runs/train/exp/weights/best.pt  --data datasets/data.yaml --source https://www.youtube.com/watch?v=wqctLW0Hb_0*

- from Video: 

*python3 yolov5/detect.py --weights yolov5/runs/train/exp/weights/best.pt  --data ../datasets/data.yaml --source media/traffic.mp4 --name video_1 --view-img*

***directories to project Daytime_project_yolov5***

 - datasets
 - media: download the folder media from google drive 
 
 link: https://drive.google.com/drive/folders/1HBzXy68X8Kg249IoYTfHPJe-6j_6JuPz?usp=sharing
 - src
 - yolov5: download the folder yolov5 from google drive 
 
 link: https://drive.google.com/drive/folders/1kFYU17MMvOpOs8O397jWA3Q44nS-wsHy?usp=sharing


3. ### YOLOv5_DeepSort_Pytorch

**Run YOLOv5 DeepSort Tracker with our datasets**

*python3 track_changed.py --source media/test2.mp4 --yolo-weights weights/best.pt  --show-vid --save-vid*

download the folder yolov5_DeepSort from google drive 
 
 link: https://drive.google.com/drive/folders/1s66jA1RQkZ5CMI1F1zYcgm4S3_xkLpK5?usp=sharing









