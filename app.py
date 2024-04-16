from flask import Flask, render_template, jsonify
import socket

app = Flask(__name__)

@app.route('/')
def home():
    container_id = socket.gethostname()  # Get the current container ID using the hostname
    return render_template('index.html', container_id=container_id)

@app.route('/health')
def health():
    # This endpoint will return a JSON response indicating that the service is up.
    return jsonify({"status": "healthy", "message": "Service is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
