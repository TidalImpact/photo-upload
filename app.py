from flask import Flask, request, send_from_directory, abort
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
UPLOAD_API_KEY = 'UPLOAD123'  # Key zum Hochladen
VIEW_API_KEY = 'VIEW456'      # Key zum Anschauen

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    auth = request.headers.get('Authorization')
    if auth != f'Bearer {UPLOAD_API_KEY}':
        return 'Unauthorized', 401

    file = request.files.get('file')
    if not file:
        return 'No file', 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return 'OK', 200

@app.route('/gallery')
def gallery():
    auth = request.headers.get('Authorization')
    if auth != f'Bearer {VIEW_API_KEY}':
        return 'Unauthorized', 401

    files = os.listdir(UPLOAD_FOLDER)
    # Einfachste Galerie: Liste der Dateien als Links
    file_links = [f'<li><a href="/gallery/{f}">{f}</a></li>' for f in files]
    return f"<h1>Gallery</h1><ul>{''.join(file_links)}</ul>"

@app.route('/gallery/<filename>')
def get_file(filename):
    auth = request.headers.get('Authorization')
    if auth != f'Bearer {VIEW_API_KEY}':
        return 'Unauthorized', 401

    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
