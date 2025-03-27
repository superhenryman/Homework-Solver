from flask import Flask, request, render_template, send_file  # Added send_file import
import pytesseract
from PIL import Image
from werkzeug.utils import secure_filename
import os
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import google.generativeai as genai

API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def plot_expression(expression, x_range=(-10, 10), output_file="graph.png"):
    x = sp.symbols('x')
    try:
        expr = sp.sympify(expression)
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"
    
    f_lambdify = sp.lambdify(x, expr, "numpy")
    x_values = np.linspace(x_range[0], x_range[1], 400)
    
    try:
        y_values = f_lambdify(x_values)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"
    
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, label=f"f(x) = {expression}", color='blue')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Graph of the Function")
    plt.legend()
    plt.savefig(output_file)
    plt.close()
    return output_file

def gen_graph_or_math_answer(text):
    try:
        response = model.generate_content(
            f"Is this a graphing question? Answer ONLY 'GRAPH' or 'NO': {text}"
        )
        ai_response = response.text.strip().upper()
        
        if ai_response == "GRAPH":
            expr_response = model.generate_content(
                f"Extract ONLY the mathematical expression from: {text}"
            )
            expression = expr_response.text.strip()
            plot_result = plot_expression(expression)
            if "Error" in plot_result:
                return plot_result
            return "Graph generated and saved as graph.png"
        else:
            math_response = model.generate_content(
                f"Answer this math question concisely: {text}"
            )
            return math_response.text
    except Exception as e:
        return f"Error generating answer: {str(e)}"

# Fixed if_graphing_or_math
def if_graphing_or_math(text):
    try:
        response = model.generate_content(
            f"Is this question about graphing or advanced math? Answer ONLY 'YES' or 'NO': {text}"
        )
        ai_response = response.text.strip().lower()
        return ai_response in ['yes', 'true', 'graph']
    except Exception as e:
        print(f"Graph check error: {str(e)}")
        return False

@app.route('/graph.png')
def serve_graph():
    return send_file('graph.png', mimetype='image/png')

# Add this missing function
def gen_general_answer(text):
    try:
        response = model.generate_content(f"Answer this question concisely: {text}")
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def main():
    if os.path.exists("graph.png"):
        try:
            os.remove("graph.png")
        except Exception as e:
            print(f"Graph cleanup error: {str(e)}")
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
            
        file = request.files['file']
        if file.filename == '':
            return "Empty filename", 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            
            text = get_image_text(path)
            if not text:
                return "OCR failed - no text found", 400
                
            try:
                if if_graphing_or_math(text):
                    answer = gen_graph_or_math_answer(text)
                    graph_generated = os.path.exists("graph.png")
                else:
                    answer = gen_general_answer(text)
                    graph_generated = False
            finally:
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"File cleanup error: {str(e)}")
            
            return render_template(
                "index.html",
                answer=answer,
                graph=graph_generated
            )
    
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_text(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip() or None
    except Exception as e:
        print(f"OCR error: {str(e)}")
        return None

if __name__ == "__main__":
    app.run(debug=True)
