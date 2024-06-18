# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 23:35:18 2024

@author: roseborod
"""

!pip install Flask

import threading
import webbrowser
from flask import Flask, render_template_string, request, jsonify

# Create the Flask app
app = Flask(__name__)

# Define the home route
@app.route('/')
def index():
    prompt = "Solve the equation: x^2 = 4"
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calculus Adventure</title>
        <script src="https://www.desmos.com/api/v1.4/calculator.js?apiKey=dcb31709b452b1cf9dc26972add0fda6"></script>
    </head>
    <body>
        <h1>Calculus Adventure</h1>
        
        <!-- Desmos Calculator -->
        <div id="calculator" style="width: 600px; height: 400px;"></div>
        
        <script>
            var elt = document.getElementById('calculator');
            var calculator = Desmos.GraphingCalculator(elt);
        </script>
        
        <!-- Quiz Form -->
        <form id="quiz-form">
            <label for="answer">Enter your answer:</label>
            <input type="text" id="answer" name="answer">
            <button type="submit">Submit</button>
        </form>
        
        <!-- Result Display -->
        <div id="result"></div>
        
        <script>
            // Initialize Desmos calculator
            var elt = document.getElementById('calculator');
            var calculator = Desmos.GraphingCalculator(elt);
            calculator.setExpression({ id: 'graph1', latex: 'y=x^2' });
            
            // Handle form submission
            document.getElementById('quiz-form').addEventListener('submit', function(event) {
                event.preventDefault();
                var answer = document.getElementById('answer').value;
                
                fetch('/submit_answer', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: 'answer=' + encodeURIComponent(answer)
                })
                .then(response => response.json())
                .then(data => {
                    var resultDiv = document.getElementById('result');
                    if (data.result === 'correct') {
                        resultDiv.innerHTML = '<p style="color: green;">Correct!</p>';
                    } else {
                        resultDiv.innerHTML = '<p style="color: red;">Incorrect. Try again!</p>';
                    }
                });
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

# Define the route for handling quiz submission
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    user_answer = request.form['answer']
    correct_answer = "4"  # eplace with the logic to get the correct answer
    if user_answer == correct_answer:
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "incorrect"})

def run_app():
    app.run(port=5000, debug=True, use_reloader=False)

# Run the Flask app in a separate thread
thread = threading.Thread(target=run_app)
thread.start()

# Open the app in a new browser tab
webbrowser.open("http://127.0.0.1:5000/")
