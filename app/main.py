import os

from flask import Flask, send_file, request
from flask_cors import CORS

from services.media import Audio, Video

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.abspath(os.getcwd())

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config["GENERATED_FOLDER"] = os.path.join(BASE_DIR, 'generated')


def upload_file():
    if 'file' not in request.files:
        return None, {'error': 'No se encontró el archivo'}, 400
    file = request.files['file']
    if file.filename == '':
        return None, {'error': 'Nombre de archivo vacío'}, 400
    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)
    return path, {'message': 'Archivo subido exitosamente'}, 200


@app.route("/transcribe", methods=['POST'])
def transcribe():
    path, _, _ = upload_file()
    _, ext = os.path.splitext(path)
    print(ext)
    if ext == ".mp4":
        return Video(path).transcribe_file()
    elif ext == ".mp3" or ext == ".wav":
        return Audio(path).transcribe_file()
    else:
        return {"message": "format no support"}


@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(app.config["GENERATED_FOLDER"], filename)
    print(file_path)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return {"error": "File not found"}, 404


@app.route("/ping")
def pong():
    return "pong"


if __name__ == '__main__':
    if not os.path.exists("generated"):
        os.mkdir("generated")
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if not os.path.exists("uploads"):
        os.mkdir("uploads")
    app.run("localhost", 3001, debug=True)
