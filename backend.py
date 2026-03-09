from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import sqlite3
import bcrypt
import random, string
load_dotenv()

webhook = os.getenv("DISCORD_WEBHOOK")
conn = sqlite3.connect("data/vm.db",check_same_thread=False)
cursor = conn.cursor()


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

# log in the administrators (works with adminLoginPage.js)
@app.route("/api/admin-login", methods=["POST"])
def admin_login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    cursor = conn.cursor()
    #this makes sure that admins are considered inactive (prevents closing browser before logging out problems)
    cursor.execute("""
        UPDATE administrators
        SET is_active = 0
        WHERE last_seen < datetime('now', '-2 minutes')
        """)
    conn.commit()
    
    #allows for checking username and password
    cursor.execute("""
    SELECT username, password, first_name, last_name
    FROM administrators
    WHERE username = ?
    """, (username,))

    #using bcrypt to make sure passwords stored in database are hashed
    user = cursor.fetchone()
    if user and bcrypt.checkpw(password.encode(), user[1].encode()):
        # mark admin as active
        cursor.execute("""
            UPDATE administrators
            SET is_active = 1,
                last_seen = CURRENT_TIMESTAMP
            WHERE username = ?
            """, (username,))
        conn.commit()
        return jsonify({
            "success": True,
            "username": user[0],
            "first_name": user[1],
            "last_name": user[2]
        })
    else:
        return jsonify({"success": False})

#handles the logout of admin works with adminHomePage.js
@app.route("/api/admin-logout", methods=["POST"])
def admin_logout():
    data = request.get_json()
    username = data.get("username")

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE administrators SET is_active = 0 WHERE username = ?",
        (username,)
    )
    conn.commit()
    return jsonify({"success": True})


#TODO: remove this function once stripe is implemented (this is purely for testing purposes, it generates a "stripe like" code)
def generate_session_id():
    return "test_" + "".join(random.choices(string.ascii_letters + string.digits, k=32))

#this generates a random code to store in database, so that we can provide users with their code after they pay
@app.route("/api/create-test-payment", methods=["POST"])
def create_test_payment():
    #gets rid of expired codes (after 24 hrs)
    conn.execute(
        """
        DELETE FROM valid_codes
        WHERE created_at < datetime('now','-24 hours')
        """
    )
    conn.commit()
    
    
    while True:
        code = f"{random.randint(0,9999):04d}"
        session_id = generate_session_id() #TODO: replace with actual Stripe session ID once Stripe is implemented

        try:
            conn.execute(
                """
                INSERT INTO valid_codes (code, stripe_session_id)
                VALUES (?, ?)
                """,
                (code, session_id)
            )
            conn.commit()

            return jsonify({
                "session_id": session_id
            })

        except sqlite3.IntegrityError:
            continue


#this gets the code associated with a stripe session id, so that we can provide users with their code after they pay  
@app.route("/api/get-code")
def get_code():

    session_id = request.args.get("session_id")

    result = conn.execute(
        """
        SELECT code
        FROM valid_codes
        WHERE stripe_session_id = ?
        AND created_at >= datetime('now','-24 hours')
        """,
        (session_id,)
    ).fetchone()

    if result is None:
        return jsonify({"error": "Code not found or expired"}), 404

    return jsonify({"code": result[0]})
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)