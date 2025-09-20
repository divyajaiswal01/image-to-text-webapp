from flask import Flask, request, jsonify, send_from_directory
import pytesseract
from PIL import Image
import os
from flask_cors import CORS

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
CORS(app)  # allow frontend JS to talk to Flask

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
FRONTEND_FOLDER = os.path.join(BASE_DIR, "..", "frontend")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('image')
    if not file or file.filename == "":
        return jsonify({"error": "No file uploaded"}), 400

    # Save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        # Open image and convert to grayscale
        img = Image.open(filepath)
        img = img.convert('L')

        # Extract text
        text = pytesseract.image_to_string(img).strip()

        # If no text is found, return a friendly message
        if not text:
            text = "[No text found in this image]"

        return jsonify({"extracted_text": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
