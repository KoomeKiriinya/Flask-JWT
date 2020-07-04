from run import app
from flask import jsonify
@app.route('/')
def index():
    return jsonify({'message':'Testing if flask is working'})