from flask import Flask, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/upload", methods=['POST'])
def upload_file():
    try:
        f = request.files['file']
        f.save(f.filename)
        data = os.popen('python3 main.py ' + f.filename).read()
        os.remove(f.filename)
        return data
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    app.run()