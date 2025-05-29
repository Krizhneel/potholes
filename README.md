The datatset have been marked and generated from Roboflow.
TO run this dataset using YOLO - Use this code:

!yolo task=detect mode=train \
    model=yolov8l.pt \
    data=../content/drive/MyDrive/Datasets/Pothole/data.yaml \
    epochs=100 \
    imgsz=640 \
    batch=16 \  # Adjusted based on your GPU memory
    patience=20 \  # Early stopping to prevent overfitting
    optimizer='AdamW' \  # Better optimizer for most cases
    lr0=0.001 \  # Initial learning rate
    lrf=0.01 \  # Final learning rate (1% of lr0)
    weight_decay=0.0005 \  # Regularization
    hsv_h=0.015 \  # Image augmentation
    hsv_s=0.7 \
    hsv_v=0.4 \
    degrees=10.0 \  # Rotation augmentation
    translate=0.1 \  # Translation augmentation
    scale=0.5 \  # Scale augmentation
    shear=2.0 \
    flipud=0.5 \  # Flip up-down probability
    fliplr=0.5 \  # Flip left-right probability
    mosaic=1.0 \  # Mosaic augmentation probability
    mixup=0.1 \  # Mixup augmentation probability
    copy_paste=0.1 \  # Copy-paste augmentation
    name='pothole_detection_v1'  # Custom run name


INSTALLATIONS REQUIRED:
!pip install ultralytics
