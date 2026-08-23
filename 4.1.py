
    
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os

# ==============================
#   TOOL GỬI GMAIL - TOKY
# ==============================

# Cấu hình sẵn Gmail của bạn
SENDER_EMAIL = "hc463774@gmail.com"      # Gmail của bạn
APP_PASSWORD = "bczk stfa panj uprc"         # Mật khẩu ứng dụng Gmail (16 ký tự)

os.system("cls" if os.name == "nt" else "clear")

print("═════════════════════════════════════════════")
print("         💌 TOOL GỬI GMAIL - TOKY 💌")
print("═════════════════════════════════════════════")
print("⚠️ Lưu ý:")
print(" - Spam gmail V1")
print(" - Admin : KTool & Toky")
print(" - KTool và Toky là 1!")
print("═════════════════════════════════════════════\n")

# ===== NHẬP THÔNG TIN =====
receiver_email = input("[~] Nhập Gmail người nhận: ")
subject = input("[~] Nhập tiêu đề: ")
message_body = input("[~] Nhập nội dung: ")
delay = float(input("[~] Nhập delay giữa các lần gửi (giây): "))
count = int(input("[~] Nhập số lần gửi: "))

# ===== GỬI EMAIL =====
print("\n📤 Bắt đầu gửi...")

success = 0
fail = 0

for i in range(count):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message_body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        success += 1
        print(f"✅ [{i+1}/{count}] Gửi thành công tới {receiver_email}")
    except Exception as e:
        fail += 1
        print(f"❌ [{i+1}/{count}] Gửi thất bại! Lỗi:", e)

    if i != count - 1:
        time.sleep(delay)

print("\n═════════════════════════════════════════════")
print(f"📊 Hoàn tất! Thành công: {success} | Thất bại: {fail}")
print("═════════════════════════════════════════════")
print("Cảm ơn bạn đã sử dụng tool TOKY 💖")
print("═════════════════════════════════════════════")
