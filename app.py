import os
from flask import Flask, request, send_from_directory, abort, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
UPLOAD_API_KEY = 'UPLOAD123'
VIEW_API_KEY = 'VIEW456'

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
    file_links = [f'<li><a href="/gallery/{f}">{f}</a></li>' for f in files]
    return f"<h1>Gallery</h1><ul>{''.join(file_links)}</ul>"

@app.route('/gallery/<filename>')
def get_file(filename):
    auth = request.headers.get('Authorization')
    if auth != f'Bearer {VIEW_API_KEY}':
        return 'Unauthorized', 401

    return send_from_directory(UPLOAD_FOLDER, filename)




@app.route('/getgallery')
def get_gallery_json():
    auth = request.headers.get('Authorization')
    if auth != f'Bearer {VIEW_API_KEY}':
        return 'Unauthorized', 401

    # In-Memory ZIP erstellen
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, mode='w') as zf:
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                zf.write(file_path, arcname=filename)
    mem_zip.seek(0)
    return send_file(mem_zip, mimetype='application/zip', as_attachment=True, download_name='all_images.zip')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



