from flask import Flask, request, render_template
import pytesseract
from PIL import Image
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Ensure the folder exists.

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_text(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error {e}")
        return None
    
@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template("error.html", error="You didn't upload a file.")

        file = request.files['file']
        if file.filename == "":
            return render_template("error.html", error="You didn't upload a file.")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        return render_template("index.html", answers="")
    return render_template("index.html")

