from flask import Flask, render_template, Response
import cv2
from pyzbar.pyzbar import decode
import numpy as np

app = Flask(__name__)
cap = cv2.VideoCapture(0)
scanning = False

def gen_frames():
    global scanning
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            if scanning:
                decoded_objects = decode(frame)
                for obj in decoded_objects:
                    # Draw a rectangle around the barcode
                    (x, y, w, h) = obj.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # Extract barcode data
                    barcode_data = obj.data.decode("utf-8")
                    print(barcode_data)  # Print barcode data to the console
            ret, buffer = cv2.imencode('.jpg', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_scan')
def start_scan():
    global scanning
    scanning = True
    return 'Barcode scanning started.'

@app.route('/stop_scan')
def stop_scan():
    global scanning
    scanning = False
    return 'Barcode scanning stopped.'

if __name__ == '__main__':
    app.run(debug=True)
