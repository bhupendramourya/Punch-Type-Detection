from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
import json
import os
from time import sleep
import threading

# Flask app and SocketIO setup
app = Flask(__name__)
socketio = SocketIO(app)

# Function to load stats from JSON
def load_stats():
    if not os.path.exists("detection_stats.json"):
        return {}
    with open("detection_stats.json", "r") as f:
        return json.load(f)

# Function to emit stats from the JSON file
def emit_stats():
    while True:
        stats = load_stats()  # Load latest stats from the JSON file

        # Emit stats to connected clients via SocketIO
        socketio.emit('update_stats', stats)

        sleep(1)  # Broadcast updates every second

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# SocketIO event to handle connection
@socketio.on('connect')
def handle_connect():
    print("Client connected")

# SocketIO event to handle disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

# Route to fetch stats (for initial loading or API requests)
@app.route('/stats')
def stats():
    detection_stats = load_stats()
    return jsonify(detection_stats)

# Start the stats emission in a background thread
def start_stats_emission():
    threading.Thread(target=emit_stats, daemon=True).start()

# Initialize background thread when the application starts
if __name__ == "__main__":
    start_stats_emission()  # Start stats emission before running the app
    socketio.run(app, host='0.0.0.0', port=5000)
