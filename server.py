from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import json

app = Flask(__name__)
CORS(app)

# Đảm bảo tồn tại file messages.txt
LOG_FILE = "messages.txt"
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("---- Love Messages Log ----\n\n")

@app.route("/api/love-response", methods=["POST"])
def love_response():
    try:
        data = request.get_json()
        status = data.get("status")
        message = data.get("message", "")
        user_message = data.get("userMessage", "")
        timestamp = data.get("timestamp", datetime.utcnow().isoformat())

        log_entry = {
            "timestamp": timestamp,
            "status": status,
            "message": message,
        }

        if user_message:
            log_entry["userMessage"] = user_message

        # Ghi vào messages.txt
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

        return jsonify({"success": True, "msg": "Đã ghi nhận phản hồi"}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True)
