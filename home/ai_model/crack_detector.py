from ultralytics import YOLO
from PIL import Image


# Load YOLO model
model = YOLO("yolo11n.pt")


def detect_crack(image_path):

    image = Image.open(image_path)

    results = model(image)

    detected = False

    for result in results:
        if result.boxes is not None and len(result.boxes) > 0:
            detected = True

    if detected:
        return "⚠️ Crack Detected"
    else:
        return "✅ No Crack Detected"