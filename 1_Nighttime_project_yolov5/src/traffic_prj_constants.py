import torch

path = "yolov5/runs/train/exp/weights/best.pt"
model = torch.hub.load("yolov5", "custom", path, source="local")

CAR = model.names[0] = "car"
TRUCK = model.names[1] = "truck"
COLOR_CAR = (0, 0, 255)
COLOR_TRUCK = (0, 254, 255)
COLOR_LINE = (255, 0, 0)
COLOR_TEXT = (255, 255, 255)
LINE_POSITIONAL1 = 376
LINE_POSITIONAL2 = 382
OFFSET1 = 12
OFFSET2 = 13
