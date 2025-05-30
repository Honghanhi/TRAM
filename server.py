from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

@app.route('/submit', methods=['POST'])
def submit_message():
    data = request.json
    message = data.get('message', '')

    with open("messages.txt", "a", encoding="utf-8") as file:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{time}] Tin nhắn: {message}\n")

    return jsonify({"success": True, "message": "Đã nhận lời nhắn thành công!"})

@app.route('/')
def home():
    return 'Server đang chạy OK!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
