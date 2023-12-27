from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# List to hold chat history
chat_history = []

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)