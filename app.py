from flask import Flask, render_template, request, session, make_response, jsonify
import sys
from helper.assignment import assignPeople, Person, AssignmentParams

app = Flask(__name__)
# app.secret_key = 'any random string'


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/allocation', methods=['GET'])
def allocation():
    return render_template('allocation.html', assignments=session['assignments'])


@app.route('/create', methods=['POST'])
def create():
    content = request.json
    session['rules'] = content[2]['rules']
    params = AssignmentParams(1)
    people = [Person(fname, '') for fname in content[0]['people']]
    for rule in session['rules']:
        A = [p for p in people if p.getFullName() == rule['personA']][0]
        B = [p for p in people if p.getFullName() == rule['personB']][0]
        if 'Year' not in rule:
            A.addPersonThatCantBeOn(B)
        else:
            A.addPersonHasBeenOn(B, int(rule['Year']))
    x = assignPeople(people=people, params=params)
    x = [str(p) for p in x]
    session['assignments'] = x
    response = make_response(jsonify({
        'message': 'success'
    }), 200)
    response.headers["Content-Type"] = "application/json"
    return response
