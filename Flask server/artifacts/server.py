from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/Avengers_classification', methods = ['GET', 'POST'])
def classify():
    base64_str = request.form['image_data']
    response = jsonify(util.classify_img(base64_str))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    util.load_artifacts()  # read the saved model and class dictionary
    app.run(debug = True, port=4999)
