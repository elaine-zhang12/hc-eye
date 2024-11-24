from flask import Flask, render_template, request, jsonify
from scipy.spatial import distance as dist
import time

app = Flask(__name__)

current_head_size = 222250
current_font_size = 16

@app.route('/')
def home():
    return "Welcome to home page"

@app.route('/api/head_size', methods=['POST'])
def get_head_size():
    global current_head_size
    global current_font_size
    data = request.get_json()
    head_size = data.get("head_size")
    font_size = data.get("font_size")
    current_head_size = head_size
    current_font_size = font_size
    return jsonify({"status": "success"})
 

@app.route('/api/get_font_size', methods=['GET'])
def view_head_size():
    if current_head_size is not None:
        return jsonify({"status": "success", "head_size": current_head_size, "font_size": current_font_size})
    

if __name__ == '__main__':
    app.run(debug=True)

