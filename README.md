# Punch Detection and Stats Visualization

This repository contains a real-time punch detection system that uses YOLOv7 for detecting punch types in video streams and visualizing the results via a web interface.



[Result.webm](https://github.com/user-attachments/assets/5efd1451-1832-4ef1-8e35-c3a034673345)


## Features

- **Real-time Punch Detection**: Uses YOLOv7 for detecting and classifying punches (e.g., jabs, uppercuts).
- **Live Stats Visualization**: Displays detection statistics on a responsive web UI.
- **Scalable Architecture**: Modular design allows easy integration of additional detection models or metrics.

---

## Repository Structure

```plaintext
punch-detection/
yolov7                              # YOLOv7 model and utilities
├── templates/                      # HTML templates for front-end
├── static/                         # Static assets like CSS, JS (if any)
├── detection_stats.json            # JSON file for storing detection stats
├── analytics.py                    # Backend script for YOLOv7-based analytics
├── app.py                          # Flask application with SocketIO for real-time updates
├── requirements.txt                # List of required Python packages
└── README.md                       # Documentation for this repository

```
## Setup Instructions
# Prerequisites
- Python 3.8+: Ensure Python is installed on your system.
- Dependencies: Install required Python libraries.
- YOLOv7 Weights: Download YOLOv7 pre-trained weights from the official repository.

## Installation
### Set Up a Virtual Environment:
  ```
python -m venv venv
source venv/bin/activate
```

### Install Dependencies:
```
pip install -r requirements.txt
```

## Code Explanation 

### 1. analytics.py

This file is responsible for running the YOLOv7 model for punch detection and generating real-time statistics. Below are its key components:

- Dependencies:
  
    - YOLOv7 setup: Imports YOLOv7 utilities (torch, cv2, and others) for inference.
    - JSON Handling: To store and share detection statistics with the Flask server.
      
- Configurations:
  
    - weights: Path to the YOLOv7 weights file (e.g., best.pt).
    - source: Input source (video file or webcam). Change this to "0" to use the webcam.
    - img_size, conf_thres, iou_thres: Image size, confidence threshold, and IoU threshold for YOLOv7 inference.
      
- Main Functions:
  
    - run_analytics():
        - Processes video frames through YOLOv7.
        - Detects objects (like punches) and updates detection_stats.
        - Visualizes detections on the video feed with bounding boxes and class labels.
        - Saves stats to detection_stats.json every 100 frames.
          
    - save_stats(stats):
    - 
        - Writes the current detection stats into a JSON file for use by the Flask app.
  
### 2. app.py

This file is a Flask application that serves as the back end for your real-time analytics dashboard.

- Dependencies:

  
  - Flask: Used to set up the web server and render web pages.
  - Flask-SocketIO: Enables real-time communication with the client for live stats updates.
  - JSON and OS: For reading and writing detection stats.
    
- Main Functions:
  
  - Web Routes:
    
    - @app.route('/'): Serves the main HTML page (index.html).
    - @app.route('/stats'): Provides detection statistics in JSON format.
      
  - SocketIO Events:
    
    - Handles connections (connect) and disconnections (disconnect).
    - Emits updates to clients using socketio.emit('update_stats', stats).
      
  - Background Simulation:
    
    - simulate_stats():
    - A placeholder function to simulate real-time stat updates. In your implementation, this can fetch real detection stats from analytics.py.
      
- Execution Flow:
  
    - The Flask server starts and runs on http://localhost:5000.
    - When a client connects, it receives real-time updates of detection stats via WebSockets.
 
### 3. Supporting Files

- weighs/best.pt:
  
    - This is the pre-trained YOLOv7 weights file used for inference. You need to provide this file in the repository.
      
- detection_stats.json:

  - A JSON file where analytics.py writes detection stats.
  - app.py reads this file to serve stats to clients.
  
- templates/index.html:

    -The front-end of your dashboard (not included in the upload but can be customized to display stats in a visually appealing manner).


