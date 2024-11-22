import cv2
import torch
import json
from time import sleep
from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, scale_coords
from utils.torch_utils import select_device
from torch.cuda.amp import autocast

# YOLOv7 setup
# weights = "/home/hbhcm/YOLOV7/yolov7/runs/train/yolov7_320_32/weights/best.pt"  # Adjust to your weights file path

weights = r"E:/Sponsorlytics/videoss/best_320.pt"  # Adjust to your weights file path

source = r"E:/Sponsorlytics/videoss/3.mp4"  # Use "0" for webcam or a file path for video/image
img_size = 640
conf_thres = 0.25
iou_thres = 0.45
device = ''  # Set to '0' for GPU, '' for CPU
classes = None
agnostic_nms = False
augment = False

# Initialize device and model
device = select_device(device)
model = attempt_load(weights, map_location=device)
model.to(device).eval()
stride = int(model.stride.max())
names = model.module.names if hasattr(model, 'module') else model.names
imgsz = check_img_size(img_size, s=stride)

# Load dataset
dataset = LoadImages(source, img_size=imgsz, stride=stride)

# Initialize detection stats
detection_stats = {name: 0 for name in names}


def save_stats(stats):
    """Save statistics to a JSON file for Flask to read."""
    with open("detection_stats.json", "w") as f:
        json.dump(stats, f)


def run_analytics():
    """Run YOLOv7 inference and update detection stats."""
    global detection_stats
    frame_count = 0

    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device).float() / 255.0  # Move tensor to the device and scale it
        if len(img.shape) == 3:
            img = img[None]

        try:
            # Perform inference with mixed precision (autocast) to save memory
            with torch.no_grad():
                with autocast():
                    pred = model(img, augment=augment)[0]

            # Apply NMS
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes=classes, agnostic=agnostic_nms)

            # Process detections
            for det in pred:
                if len(det):
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
                    for *xyxy, conf, cls in det:
                        cls_name = names[int(cls)]
                        detection_stats[cls_name] += 1
                        label = f"{cls_name} {conf:.2f}"
                        cv2.rectangle(im0s, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)
                        cv2.putText(im0s, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        except torch.cuda.OutOfMemoryError:
            print("CUDA out of memory. Attempting to clear cache and retry...")
            torch.cuda.empty_cache()  # Clear unused GPU memory
            continue  # Skip to next frame

        # Save updated stats to the JSON file every 100 frames
        frame_count += 1
        if frame_count % 1 == 0:
            save_stats(detection_stats)

        # Display frame
        cv2.imshow("Punch Detection", im0s)

        # Quit on 'q'
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            return

        # Add a short delay to simulate real-time processing
        sleep(1 / 30)  # Adjust to control FPS (e.g., 30 FPS)


if __name__ == "__main__":
    run_analytics()
