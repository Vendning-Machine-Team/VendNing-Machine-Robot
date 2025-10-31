import cv2 as cv
import config
from ultralytics import YOLO as yol
from typing import List, Dict, Optional, Union

class DetectionFramework:
    def __init__(self) -> None:
        self.model_path: Optional[str] = getattr(config, "PATHFINDING_MODEL_PATH", None)
        self.video_source: Union[str, List[str]] = getattr(config, "VIDEO_SOURCE", getattr(config, "IP_STREAMS", []))

        if not self.model_path:
            raise ValueError("PATHFINDING_MODEL_PATH is not defined in config.py")
        if not self.video_source:
            raise ValueError("VIDEO_SOURCE or IP_STREAMS is not defined in config.py")

        self.model: yol = yol(self.model_path)
        self.captures: Dict[str, cv.VideoCapture] = self._init_captures()

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