import os
import cv2
import numpy as np
from pathlib import Path

def apply_motion_blur(image, degree=10, angle=0):
    """Apply motion blur with estimated speed ranges"""
    k = np.zeros((degree, degree))
    k[int((degree - 1)/2), :] = np.ones(degree)
    k = cv2.warpAffine(k, cv2.getRotationMatrix2D((degree/2 - 0.5, degree/2 - 0.5), angle, 1.0), (degree, degree))  
    k = k * (1.0/np.sum(k))
    return cv2.filter2D(image, -1, k)

def process_folder(input_folder, output_base_folder):
    # Blur configurations with estimated speed ranges
    # (assuming standard shutter speed of ~1/250s)
    blur_configs = {
        'low_speed': {
            'degree': 5,
            'speed_range': '10-30 km/h (6-18 mph)',
            'description': 'Parking, residential areas'
        },
        'medium_speed': {
            'degree': 10,
            'speed_range': '30-60 km/h (18-37 mph)',
            'description': 'Urban streets'
        },
        'high_speed': {
            'degree': 15,
            'speed_range': '60-100+ km/h (37-62+ mph)',
            'description': 'Highways, freeways'
        }
    }

    os.makedirs(output_base_folder, exist_ok=True)

    for label, config in blur_configs.items():
        output_folder = os.path.join(output_base_folder, label)
        os.makedirs(output_folder, exist_ok=True)

        print(f"\nProcessing {label} category:")
        print(f"- Blur degree: {config['degree']}")
        print(f"- Estimated speed: {config['speed_range']}")
        print(f"- Typical scenario: {config['description']}")

        for filename in os.listdir(input_folder):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(input_folder, filename)
                image = cv2.imread(image_path)

                blurred = apply_motion_blur(image, degree=config['degree'], angle=0)
                output_path = os.path.join(output_folder, filename)
                cv2.imwrite(output_path, blurred)
                print(f"  Processed: {filename}")

# Example usage
script_dir = Path(__file__).parent.absolute()
input_folder = script_dir / "Images"
output_base_folder = script_dir / "blurred_images"
process_folder(input_folder, output_base_folder)