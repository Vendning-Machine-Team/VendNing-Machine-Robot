from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import sqlite3
load_dotenv()

webhook = os.getenv("DISCORD_WEBHOOK")
conn = sqlite3.connect("data/admin.db")
def SEND_AUDIT_LOG(message,urgency): # Urgency can be "True" or "False", true for when pinging @eveyrone, false for normal messages
    ret = "@everyone\n" if urgency else ""
    ret += message

    message_data = {
        "content": ret,
    }

    try:
        response = requests.post(webhook, json=message_data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending webhook: {e}")
app = Flask(
    __name__,
    static_folder="./dist",
    static_url_path=""
)

# Enable CORS (safe for dev, adjust for prod)
CORS(app)


@app.route("/api/message", methods=["POST"])
def receive_message():
    data = request.get_json()
    text = data.get("text")

    # print("Received from frontend:", text)
    SEND_AUDIT_LOG(f"Received message from frontend: {text}", False)
    return jsonify({
        "reply": f"Backend received: {text}"
    })

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")


# Handle React/Vite routing (important)
@app.route("/<path:path>")
def serve_static_files(path):
    file_path = os.path.join(app.static_folder, path)

    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        # fallback to index.html for SPA routing
        return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)