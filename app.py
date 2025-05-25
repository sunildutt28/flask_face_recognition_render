from flask import Flask, render_template, request, redirect, url_for
import face_recognition
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
KNOWN_FOLDER = 'static/known'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load known faces
known_face_encodings = []
known_face_names = []

for filename in os.listdir(KNOWN_FOLDER):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(KNOWN_FOLDER, filename)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(os.path.splitext(filename)[0])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            unknown_image = face_recognition.load_image_file(filepath)
            unknown_encodings = face_recognition.face_encodings(unknown_image)

            name = "Unknown"
            if unknown_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, unknown_encodings[0])
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

            return render_template("index.html", filename=filename, name=name)

    return render_template("index.html", filename=None)

if __name__ == "__main__":
    app.run(debug=True)
