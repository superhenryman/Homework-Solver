from flask import Flask, request, render_template
import pytesseract
from PIL import Image
from werkzeug.utils import secure_filename
import os
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import google.generativeai as genai
# plankton moan sfx
API_KEY = os.getenv("API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def plot_expression(expression, x_range=(-10, 10), output_file="graph.png"):
    x = sp.symbols('x')
    expr = sp.sympify(expression)
    
    f_lambdified = sp.lambdify(x, expr, "numpy")
    
    x_values = np.linspace(x_range[0], x_range[1], 400)
    y_values = f_lambdified(x_values)
    
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
    print(f"Graph saved as {output_file}")

def gen_graph_or_math_answer(text):
    try:
        response = model.generate_content(f"Please answer these questions {text} in a direct fashion, do not say anything else other than the answer in a format of 1- answer, 2- etc... If the input is a graphing question, return 'GRAPH'.")
        ai_response = response.text.strip()
        
        if ai_response == "GRAPH":
            plot_expression(text)
            return "Graph generated and saved as graph.png"
        else:
            return ai_response
    except Exception as e:
        return f"Unexpected error occurred while generating the answer, {e}"

def gen_general_answer(text):
    try:
        response = model.generate_content(f"Please provide the answers for this {text}, try parsing as much as you can.  in a direct fashion, do not say anything else other than the answer in a format of 1- answer, 2- etc...")
        ai_response = response.text  
        print(ai_response) # debugging
        return ai_response
    except Exception as e:
        print(f"Unexpected error occured while checking if the answer is a graphing or math question, {e}")
        return f"Unexpected error occured while generating the answer, {e}"

def if_graphing_or_math(text):
    try:
        response = model.generate_content(f"Are these questions graphing related? {text}, If they are, reply with 'True', or reply with 'False', DO NOT USE ANY PUNCTUATION!")
        ai_response = response.text
        if ai_response == "True":
            return True
        elif ai_response == "False":
            return False
        else:
            return None
    except Exception as e:
        print(f"Unexpected error occured while checking if the answer is a graphing or math question, {e}")
        return f"Unexpected error occured while checking if the answer is a graphing or math question, {e}"
    
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
filenames = []
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
    
@app.route("/free")
def free_everything():
    for filename in filenames:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    graph_path = "graph.png"
    if os.path.exists(graph_path):
        os.remove(graph_path)
    
    filenames.clear()

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == "":
            return "You didn't upload a file", 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filenames.append(filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            text = get_image_text(path)
            if if_graphing_or_math(text):
                mathanswers = gen_graph_or_math_answer(text)
                return render_template("index.html", answers=mathanswers), 200
            else:
                answer = gen_general_answer(text)
                return render_template("index.html", answers=answer), 200
    return render_template("index.html") 


