import cv2 as cv
import config
from ultralytics import YOLO as yol
from typing import List, Dict, Optional, Union

import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path: sys.path.append(parent_dir)

import webhook_output

thresholds = config.DISTANCE_THRESHOLD
width_threshold = thresholds["WIDTH"]
height_threshold = thresholds["HEIGHT"]

class DetectionFramework:
    def __init__(self) -> None:
        self.model_path: Optional[str] = getattr(config, "PATHFINDING_MODEL_PATH", None)
        self.video_source: Union[str, List[str]] = getattr(config, "VIDEO_SOURCE", getattr(config, "IP_STREAMS", []))

        if not self.model_path:
            raise ValueError("PATHFINDING_MODEL_PATH is not defined in config.py")
        if not self.video_source:
            raise ValueError("VIDEO_SOURCE or IP_STREAMS is not defined in config.py")

        self.model: yol = yol(self.model_path, verbose=False)
        self.captures: Dict[str, cv.VideoCapture] = self._init_captures()
        self.objects_close: bool = False

    def _init_captures(self) -> Dict[str, cv.VideoCapture]:
        captures: Dict[str, cv.VideoCapture] = {}
        sources = [self.video_source] if isinstance(self.video_source, str) else self.video_source

        for source in sources:
            cap = cv.VideoCapture(source)
            if not cap.isOpened():
                print(f"[ERROR] Failed to connect to video source: {source}. Skipping.")
                continue
            captures[source] = cap
        return captures

    def run(self) -> None:
        if not self.captures:
            print("[ERROR] No video sources are available. Exiting.")
            return

        while True:
            for source, cap in self.captures.items():
                ret, frame = cap.read()
                if not ret:
                    continue

                results = self.model(frame)
                annotated_frame = results[0].plot()

                cv.imshow(f"Source: {source}", annotated_frame)
                
                boxesCoords = results[0].boxes.xyxy.cpu().numpy()

                centers = []
                for box in boxesCoords:
                    x1, y1, x2, y2 = box
                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)
                    centers.append((center_x, center_y))

                    cv.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                    
                    logddddddd = True
                    for i in range(len(centers)):
                        for j in range(i + 1, len(centers)):
                            dist_x = abs(centers[i][0] - centers[j][0]) / config.CAMERA_C["IMAGE_WIDTH"]
                            dist_y = abs(centers[i][1] - centers[j][1]) / config.CAMERA_C["IMAGE_HEIGHT"]

                            if dist_x < width_threshold and dist_y < height_threshold:
                                if logddddddd:
                                    logddddddd = False
                                    webhook_output.SEND_AUDIT_LOG("Temporary testing log, only sending one because i dont want discord ratelimiting us", True)
                
            if cv.waitKey(1) & 0xFF == ord("q"):
                break

        self.cleanup()

    def cleanup(self) -> None:
        for cap in self.captures.values():
            cap.release()
        cv.destroyAllWindows()

def main() -> None:
    try:
        framework = DetectionFramework()
        framework.run()
    except (ValueError, Exception) as e:
        print(f"[CRITICAL] Error: {e}")

if __name__ == "__main__":
    main()