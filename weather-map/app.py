import os
from flask import Flask, send_from_directory, jsonify

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

@app.route('/')
def index():
    return send_from_directory('static', 'leaflet.html')

@app.route('/data/<path:filename>')
def data(filename):
    return send_from_directory(DATA_DIR, filename)

@app.route('/list')
def list_files():
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    return jsonify(sorted(files))

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=True)
