#sza250425
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import ssl

app = Flask(__name__)
#CORS(app, resources={r"/log": {"origins": "https://serzhyale.github.io"}})
CORS(app, resources={r"/log": {"origins": "*"}})

LOG_FILE = "logs.txt"

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        f.write("Life Span\n\n")

API_KEY = "25021980064500"

@app.route('/log', methods=['POST', 'OPTIONS'])
def log_message():
    if request.method == 'OPTIONS':
        return jsonify({"status": "success", "message": "OPTIONS request handled"}), 200

    api_key = request.headers.get('X-API-Key')
    if api_key != API_KEY:
        return jsonify({"status": "error", "message": "Invalid API key"}), 401

    try:
        data = request.get_json()
        message = data.get('log', '')

        client_ip = request.remote_addr
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {client_ip} - {message}\n"

        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        return jsonify({"status": "success", "message": "Log saved"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Настройка SSL-контекста
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #context.load_cert_chain(certfile='C:/Certbot/live/mylifespanlog.com/fullchain.pem', 
    #                       keyfile='C:/Certbot/live/mylifespanlog.com/privkey.pem')
    
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True, ssl_context=context)
    
    #app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
