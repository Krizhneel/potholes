import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os
from pathlib import Path

def convert_to_nighttime(image_path, output_path):
    """
    Convert a daytime image to a nighttime version
    :param image_path: path to input image
    :param output_path: path to save nighttime version
    """
    # Load the image
    img = cv2.imread(image_path)
    
    # Convert to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Reduce value (brightness) channel
    hsv[:,:,2] = hsv[:,:,2] * 0.2  # Reduce brightness
    
    # Convert back to BGR
    night_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # Add a blue-ish tint to simulate night
    night_img = cv2.addWeighted(night_img, 0.4, 
                               np.full(night_img.shape, [30, 30, 90], dtype=np.uint8), 
                               0.1, 0)
    
    # Add some noise to simulate low-light conditions
    # noise = np.random.normal(0, 1, night_img.shape).astype(np.uint8)
    # night_img = cv2.add(night_img, noise)
    
    # Reduce contrast slightly
    night_img = cv2.convertScaleAbs(night_img, alpha=0.7, beta=0)
    
    # Save the result
    cv2.imwrite(output_path, night_img)

def batch_convert_to_nighttime(input_dir, output_dir):
    """
    Convert all images in a directory to nighttime versions
    :param input_dir: directory with daytime images
    :param output_dir: directory to save nighttime images
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"night_d_{filename}")
            convert_to_nighttime(input_path, output_path)
            print(f"Processed {filename}")



script_dir = Path(__file__).parent.absolute()
batch_convert_to_nighttime( script_dir / "Images",  script_dir / "Night"  / "night_darker")