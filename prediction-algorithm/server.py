from flask import Flask, request
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
@cross_origin()
def hello():
    return "Hello World!"

@app.route("/upload", methods=['POST'])
@cross_origin()
def upload_file():
    request.headers.add("Access-Control-Allow-Origin", "*")
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