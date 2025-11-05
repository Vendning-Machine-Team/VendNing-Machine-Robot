SIZE_THRESHOLD = 1.524 # In meters

CAMERA_C = {
    "IMAGE_WIDTH": 1920,
    "IMAGE_HEIGHT": 1080,
    "FPS": 30,
}

DISTANCE_THRESHOLD = {
    "WIDTH": SIZE_THRESHOLD/CAMERA_C["IMAGE_WIDTH"], # 1.524 meters is 5 feet in pixels, divided by width of the camera, which gives an estimation for how wide, or "close" objects are.
    "HEIGHT": SIZE_THRESHOLD/CAMERA_C["IMAGE_HEIGHT"],
}

PATHFINDING_MODEL_PATH = "pathfinding/YOLOv8n.pt"

# Use a local video file as the source
VIDEO_SOURCE = f"/Users/cayden/Downloads/file.MOV"

# Or, use IP camera streams
# IP_STREAMS = ["http://your.camera.ip:port/video"]