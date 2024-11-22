# Punch Detection and Stats Visualization

This repository contains a real-time punch detection system that uses YOLOv7 for detecting punch types in video streams and visualizing the results via a web interface.

## Features

- **Real-time Punch Detection**: Uses YOLOv7 for detecting and classifying punches (e.g., jabs, uppercuts).
- **Live Stats Visualization**: Displays detection statistics on a responsive web UI.
- **Scalable Architecture**: Modular design allows easy integration of additional detection models or metrics.

---

## Repository Structure

```plaintext
punch-detection/
├── yolov7/                         # YOLOv7 model and utilities
├── templates/                      # HTML templates for front-end
├── static/                         # Static assets like CSS, JS (if any)
├── detection_stats.json            # JSON file for storing detection stats
├── analytics.py                    # Backend script for YOLOv7-based analytics
├── app.py                          # Flask application with SocketIO for real-time updates
├── requirements.txt                # List of required Python packages
└── README.md                       # Documentation for this repository
