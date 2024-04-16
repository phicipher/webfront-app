from flask import Flask, render_template, jsonify
from flask_talisman import Talisman
import socket
import logging
from version import __version__

app = Flask(__name__)

# Setup Talisman
talisman = Talisman(
    app,
    content_security_policy= {
    'default-src': [
        '\'self\'',
        'http://localhost:8080'      # Allow local server during development
    ]
                            },
    force_https=False                # Disabling HTTPS enforcement for Docker testing
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def home():
    try:
        container_id = socket.gethostname()  # Get the current container ID using the hostname
        logging.info("Home page accessed, displaying container ID.")
        return render_template('index.html', container_id=container_id, version=__version__)
    except Exception as e:
        logging.error("Error accessing home page: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500

@app.route('/health')
def health():
    logging.info("Health check accessed.")
    return jsonify({"status": "healthy", "message": "Service is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)