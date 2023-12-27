from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# List to hold chat history
chat_history = []

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
# app.config['UPLOAD_FOLDER'] = 'uploads'
# @app.route('/upload', methods=['POST'])
# def upload():
#     print("here")
#     if request.method == 'POST':
#         uploaded_files = request.files.getlist('file')
#         file_paths = []
#         for file in uploaded_files:
#             if file.filename != '':
#                 file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#                 file.save(file_path)
#                 file_paths.append(file_path)
#         return {'uploaded_files': file_paths}


if __name__ == '__main__':
    app.run(debug=True)