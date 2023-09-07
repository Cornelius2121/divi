from flask import Flask, render_template, request, session, make_response, jsonify
import sys

app = Flask(__name__)
app.secret_key = 'any random string'


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/create', methods=['POST'])
def create():
    content = request.json
    session['rules'] = content
    # function call
    response = make_response(jsonify({
        'message': 'success'
    }), 200)
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(port=8000)
