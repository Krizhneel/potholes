import cv2
import math
import cvzone
from ultralytics import YOLO
from pathlib import Path

# Get the current script's directory
script_dir = Path(__file__).parent.absolute()

# Define paths
# weights_path = script_dir / "Weights" / "GCModel.pt"
weights_path = script_dir / "Weights" / "best.pt"

input_folder = script_dir / "Media"
output_folder = script_dir / "Output"

# Load the model
yolo_model = YOLO(str(weights_path))

# Define class names
class_labels = ['Pothole']

# Create output folder if it doesn't exist
output_folder.mkdir(exist_ok=True)

# Supported image extensions
supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')

# Process all images in the input folder
for image_path in input_folder.glob('*'):
    if image_path.suffix.lower() in supported_extensions:
        # Read the image
        img = cv2.imread(str(image_path))
        
        if img is None:
            print(f"Could not find image: {image_path.name}")
            continue

        # Perform object detection
        results = yolo_model(img)

        # Loop through the detections and draw bounding boxes
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                w, h = x2 - x1, y2 - y1
                
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])

                if conf > 0.3 and cls < len(class_labels):
                    cvzone.cornerRect(img, (x1, y1, w, h), t=2)
                    cvzone.putTextRect(img, f'{class_labels[cls]} {conf}', 
                                    (x1, y1 - 10), scale=0.8, 
                                    thickness=1, colorR=(255, 0, 0))
        
        # Save the processed image
        output_path = output_folder / f"detected_{image_path.name}"
        cv2.imwrite(str(output_path), img)
        print(f"Processed: {image_path.name}")