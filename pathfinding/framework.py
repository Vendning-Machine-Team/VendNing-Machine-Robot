import cv2 as cv
import config
from ultralytics import YOLO as yol

yolo = yol(config.PATHFINDING_MODEL_PATH)

test_images = [cv.imread("pathfinding/testimage.jpg"),
               cv.imread("pathfinding/image0.jpeg"),
               cv.imread("pathfinding/image0 (1).jpeg")]

image_scans = [yolo(img) for img in test_images]
for i, scan in enumerate(image_scans):
    result_img = scan[0].plot()
    cv.imshow(f"Result Image {i+1}", result_img)

cv.waitKey(0)
cv.destroyAllWindows()