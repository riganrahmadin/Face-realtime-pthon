from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # Gunakan 0 untuk webcam

def generate_frames():
    while True:
        success, frame = camera.read()  # Baca frame dari kamera
        if not success:
            break
        else:
            # Ubah frame ke grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Gunakan cascade classifier untuk pendeteksian wajah
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            # Gambar kotak di sekitar wajah
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Encode frame dalam format JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Gunakan yield untuk mengirim frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')  # Halaman untuk menampilkan video

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
