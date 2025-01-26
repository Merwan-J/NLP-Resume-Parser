import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from resume_parser import parse_resume


app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename):
    extension_exists =  '.' in filename
    extension_valid = filename.rsplit(".")[-1].lower() in ALLOWED_EXTENSIONS

    return extension_exists and extension_valid


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)        
        
        if not filename.lower().endswith('.pdf'):
            return jsonify({"error": "Unsupported file type"}), 400
        parsed_resume = parse_resume(file)
        
        return jsonify(parsed_resume)
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True)