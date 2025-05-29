import os
import cv2
import numpy as np
from pathlib import Path
import random

def add_rain_effect(image, intensity=0.5, angle=5, drop_length=15, drop_width=1):
    """
    Add realistic rain effect to an image
    
    Args:
        image: Input image (BGR format)
        intensity: Rain intensity (0.1 to 1.0)
        angle: Rain falling angle in degrees
        drop_length: Maximum length of rain drops
        drop_width: Width of rain drops
        
    Returns:
        Image with rain effect
    """
    # Create a blank rain layer
    rain_layer = np.zeros_like(image, dtype=np.float32)
    height, width = image.shape[:2]
    
    # Calculate number of rain drops based on intensity
    num_drops = int(intensity * width * height / 100)
    
    # Generate random rain drops
    for _ in range(num_drops):
        # Random position
        x = random.randint(0, width)
        y = random.randint(0, height)
        
        # Random length (shorter when farther away)
        length = random.randint(5, drop_length)
        length = int(length * (1 - y/height))
        
        if length < 2:
            continue
            
        # Add rain drop
        end_x = x + int(length * np.sin(np.radians(angle)))
        end_y = y + int(length * np.cos(np.radians(angle)))
        
        cv2.line(rain_layer, (x, y), (end_x, end_y), 
                (200, 200, 200), drop_width, lineType=cv2.LINE_AA)
    
    # Add motion blur to rain
    rain_layer = cv2.GaussianBlur(rain_layer, (3, 3), 0)
    
    # Blend with original image
    result = cv2.addWeighted(image.astype(np.float32), 1, 
                            rain_layer, 0.7, 0)
    
    # Add overall wet look
    result = cv2.addWeighted(result, 0.9, 
                           np.full_like(result, (10, 10, 30)), 
                           0.1, 0)
    
    # Add slight brightness reduction
    result = cv2.convertScaleAbs(result, alpha=0.95, beta=-5)
    
    return result.astype(np.uint8)

def process_folder(input_folder, output_folder, intensity=0.5):
    """
    Process all images in a folder to add rain effects
    
    Args:
        input_folder: Path to input images
        output_folder: Where to save rainy images
        intensity: Rain intensity (0.1 to 1.0)
    """
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Load image
            img_path = os.path.join(input_folder, filename)
            image = cv2.imread(img_path)
            image = add_fog_effect(image)
            if image is not None:
                # Add rain effect with slight random variations
                
                rain_intensity = intensity * random.uniform(0.8, 1.2)
                # rainy_image = add_rain_effect(image, 
                #                             intensity=rain_intensity,
                #                             angle=random.randint(10, 20),
                #                             drop_length=random.randint(12, 18))
                
                rainy_image = add_rain_effect(image)
                
                
                # Save result
                output_path = os.path.join(output_folder, f"rain_{filename}")
                cv2.imwrite(output_path, rainy_image)
                print(f"Added rain to: {filename}")
            else:
                print(f"Failed to load: {filename}")
                
def add_fog_effect(image, intensity=0.8):
    """Add atmospheric fog effect"""
    fog = np.full_like(image, (170, 170, 170))
    return cv2.addWeighted(image, 1-intensity, fog, intensity, 0)

if __name__ == "__main__":
    # Configuration
    script_dir = Path(__file__).parent.absolute()
    input_folder = script_dir / "Images"
    output_folder = script_dir / "rainy_potholes"
    
    # Adjust rain intensity (0.1 = light rain, 1.0 = heavy rain)
    rain_intensity = 0.5
    
    # Run processing
    process_folder(input_folder, output_folder, intensity=rain_intensity)
    print(f"\nRain effect added to images. Results saved to: {output_folder}")
    