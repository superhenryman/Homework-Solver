import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import google.generativeai as genai
import os
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
        response = model.generate_content(f"Please answer these questions {text} in a direct fashion, do not say anything else other than the answer in a format of 1- answer, 2- etc... If the input is a math function, return 'GRAPH'.")
        ai_response = response.text.strip()
        
        if ai_response == "GRAPH":
            plot_expression(text)
            return "Graph generated and saved as graph.png"
        else:
            return ai_response
    except Exception as e:
        return f"Unexpected error occurred while generating the answer, {e}"
