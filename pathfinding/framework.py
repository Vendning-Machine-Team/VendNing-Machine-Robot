import cv2 as cv
import config
from ultralytics import yol

yolo = yol.YOLO(config.PATHFINDING_MODEL_PATH)

