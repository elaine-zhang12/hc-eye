from flask import Flask, render_template, request, jsonify
from scipy.spatial import distance as dist
import time

app = Flask(__name__)

current_head_size = 222250

@app.route('/')
def home():
    return "Welcome to home page"

@app.route('/api/head_size', methods=['POST'])
def get_head_size():
    global current_head_size
    data = request.get_json()
    head_size = data.get("head_size")
    current_head_size = head_size
    return jsonify({"status": "success"})
 

@app.route('/api/get_font_size', methods=['GET'])
def view_head_size():
    if current_head_size is not None:
        font_size = 300
        return jsonify({"status": "success", "head_size": current_head_size, "font_size": font_size})
    

if __name__ == '__main__':
    app.run(debug=True)

