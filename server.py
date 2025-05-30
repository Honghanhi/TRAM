from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import json
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

LOG_FILE = "messages.txt"
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("---- Love Messages Log ----\n\n")

# Cấu hình email của bạn (sử dụng Gmail hoặc dịch vụ SMTP khác)
EMAIL_SENDER = 'youremail@gmail.com'
EMAIL_PASSWORD = 'your_app_password'  # App password, không phải mật khẩu Gmail thường
EMAIL_RECEIVER = 'youremail@gmail.com'  # Gửi cho chính bạn

def send_email(subject, content):
    try:
        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("❌ Lỗi gửi email:", e)
        return False

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

        # Gửi email
        subject = f"[Y] Phản hồi mới: {status.upper()}"
        content = f"""Thời gian: {timestamp}
Trạng thái: {status}
Tin nhắn: {message}
Người dùng viết: {user_message}
"""
        send_email(subject, content)

        return jsonify({"success": True, "msg": "Đã ghi nhận phản hồi"}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Tùy chọn: endpoint riêng để test email
@app.route("/api/send-email", methods=["POST"])
def manual_email():
    try:
        data = request.get_json()
        subject = data.get("subject", "Tin nhắn từ Y")
        content = data.get("content", "Không có nội dung")
        result = send_email(subject, content)
        if result:
            return jsonify({"success": True, "msg": "Đã gửi email"}), 200
        else:
            return jsonify({"success": False, "msg": "Lỗi khi gửi email"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
