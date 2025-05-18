from flask import Flask, render_template, Response, request, redirect
import os
from face_utils import VideoCamera, train_model

app = Flask(__name__)
os.makedirs('static/faces', exist_ok=True)

# Globals for state
camera = None
current_name = None
mode = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    global camera, current_name, mode
    if request.method == 'POST':
        current_name = request.form['name']
        mode = 'register'
        camera = VideoCamera(mode, current_name)
        return render_template('camera.html', mode='Registering', action='/')
    return render_template('register.html')


@app.route('/detect')
def detect():
    global camera, current_name, mode
    mode = 'detect'
    current_name = None
    camera = VideoCamera(mode)
    return render_template('camera.html', mode='Detecting', action='/')

@app.route('/video_feed')
def video_feed():
    global camera
    return Response(camera.get_frame_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
