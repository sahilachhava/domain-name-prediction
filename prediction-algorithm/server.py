from flask import Flask, request
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/upload", methods=['POST'])
@cross_origin()
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
    

@app.route("/uploadTextInput", methods=['POST'])
@cross_origin()
def upload_textInput():
    try:
        f = request.get_data()
        # f.save(f.filename)
        # data = os.popen('python3 main.py ' + f.filename).read()
        # os.remove(f.filename)
        return f
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    app.run()