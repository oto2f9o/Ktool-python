
# --- END UPDATED KTool.py ---

#!/usr/bin/env python3
# coding: utf-8
"""
TOOL GỬI GMAIL - TOKY v6
- Mỗi vòng: tất cả tài khoản gửi tới 1 tài khoản đích
- Gửi đồng thời (multithreading) -> nhanh hơn
- Hỗ trợ nhiều tiêu đề và nhiều nội dung, lặp vòng theo modulo
- SENDER_ACCOUNTS: sửa trực tiếp trong file (["email","app_password"])
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time, os, sys, traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# ==== MÀU ====
RESET = "\033[0m"; BOLD = "\033[1m"
RED = "\033[31m"; GREEN = "\033[32m"; YELLOW = "\033[33m"
CYAN = "\033[36m"; MAGENTA = "\033[35m"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_TIMEOUT = 30  # giây

# ==== DANH SÁCH TÀI KHOẢN (SỬA Ở ĐÂY) ====
SENDER_ACCOUNTS = [
    ["hc463774@gmail.com", "bczkstfapanjuprc"],
    ["nonamenay123@gmail.com", "xczylscivmdpamcr"],
    ["le8818666@gmail.com", "zjuuoixfhxpkamst"],
    ["nonameday520@gmail.com", "btzaxtjruinbooym"],
    ["lehuunhan45611@gmail.com", "fjjmwjijiugbpqzu"],
    ["nonamene1314@gmail.com", "txauvlyobvkbnznf"],
]
# ==========================

PRINT_LOCK = Lock()
LOG_LOCK = Lock()

def mask_email(email):
    """Ẩn phần giữa của email để tránh lộ thông tin."""
    try:
        name, domain = email.split("@", 1)
        if len(name) <= 3:
            return name[0] + "••••@" + domain
        return name[:3] + "••••" + name[-1:] + "@" + domain
    except:
        return email

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print(BOLD + CYAN + "═" * 70 + RESET)
    print(BOLD + MAGENTA + "        💌 TOOL GỬI GMAIL - TOKY (v6) 💌" + RESET)
    print(BOLD + CYAN + "═" * 70 + RESET)
    print(YELLOW + "📋Spam gmail V2 gửi spam nhiều tài khoản về 1 tài khoản chỉ định" + RESET)
    print(YELLOW + "👑Admin : Toky" + RESET)
    print(YELLOW + "▶️YouTube: KTool" + RESET)
    print(BOLD + CYAN + "═" * 70 + RESET + "\n")

def build_message(sender, receiver, subject, body, is_html=False):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    part = MIMEText(body, "html" if is_html else "plain")
    msg.attach(part)
    return msg

def send_single(sender_email, app_password, receiver_email, subject, body, is_html=False):
    """Hàm thực thi gửi 1 email từ 1 account. Trả về (ok:bool, error:str|None)."""
    try:
        msg = build_message(sender_email, receiver_email, subject, body, is_html=is_html)
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=SMTP_TIMEOUT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, [receiver_email], msg.as_string())
        return True, None
    except Exception as e:
        return False, str(e)

def input_list(prompt):
    items = []
    idx = 1
    while True:
        val = input(f"{BOLD}    {prompt} {idx}: {RESET}")
        if not val.strip():
            break
        items.append(val.strip())
        idx += 1
    return items

def safe_print(*args, **kwargs):
    with PRINT_LOCK:
        print(*args, **kwargs)

def main():
    banner()
    if not SENDER_ACCOUNTS:
        safe_print(RED + "❌ Chưa có tài khoản trong SENDER_ACCOUNTS. Sửa trực tiếp trong file." + RESET)
        sys.exit(1)

    safe_print(f"{BOLD}{CYAN}Đã nạp ({len(SENDER_ACCOUNTS)}) tài khoản:{RESET}")
    for i, (e, _) in enumerate(SENDER_ACCOUNTS, 1):
        safe_print(f"  {GREEN}{i}. {mask_email(e)}{RESET}")
    safe_print()

    try:
        delay = float(input(f"{BOLD}[~] Nhập delay giữa các lần gửi : {RESET}(tính bằng giây) ").strip() or "1")
        receiver = input(f"{BOLD}[~] Nhập Tài khoản Nhận Tin : {RESET}").strip()
        if not receiver:
            safe_print(RED + "❌ Người nhận rỗng. Thoát." + RESET); return

        # chế độ gửi HTML hay plain
        is_html = input(f"{BOLD}[~] Gửi dạng HTML? (y/N): {RESET}").strip().lower() in ("y","yes")

        safe_print(f"{BOLD}[~] Nhập các Tiêu đề (Enter bỏ qua để dừng):{RESET}")
        subjects = input_list("Tiêu đề")
        if not subjects:
            safe_print(RED + "❌ Phải có ít nhất 1 tiêu đề!" + RESET); return

        safe_print(f"{BOLD}[~] Nhập các Nội dung (Enter bỏ qua để dừng):{RESET}")
        bodies = input_list("Nội dung")
        if not bodies:
            safe_print(RED + "❌ Phải có ít nhất 1 nội dung!" + RESET); return

        total_rounds = int(input(f"{BOLD}[~] Nhập số lần : {RESET}").strip() or "1")
        max_workers_input = input(f"{BOLD}[~] Số luồng tối đa (hãy ấn enter = {len(SENDER_ACCOUNTS)}): {RESET}").strip()
        max_workers = int(max_workers_input) if max_workers_input.isdigit() and int(max_workers_input)>0 else len(SENDER_ACCOUNTS)

    except Exception as ex:
        safe_print(RED + "❌ Nhập sai dữ liệu! Thoát..." + RESET); return

    safe_print(CYAN + "\n[^°^] Đang tiến hành ......\n" + RESET)

    overall_success = 0
    overall_fail = 0
    error_logs = []

    # ThreadPoolExecutor sẽ dùng max_workers luồng để gửi song song trong mỗi vòng
    for round_idx in range(total_rounds):
        safe_print(YELLOW + f"🌀 Vòng gửi {round_idx+1}/{total_rounds} - sử dụng subject index {round_idx % len(subjects)} và body index {round_idx % len(bodies)}" + RESET)
        subject = subjects[round_idx % len(subjects)]
        body = bodies[round_idx % len(bodies)]

        futures = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for acc_idx, (sender_email, app_password) in enumerate(SENDER_ACCOUNTS, 1):
                # submit một task cho mỗi tài khoản
                futures.append(
                    executor.submit(
                        send_single,
                        sender_email, app_password, receiver, subject, body, is_html
                    )
                )

            # thu thập kết quả khi hoàn thành
            for i, fut in enumerate(as_completed(futures), 1):
                ok, err = fut.result()
                # i không đảm bảo tương ứng acc_idx; hiển thị theo thứ tự hoàn thành
                # để biết chính xác account nào, ta có thể wrap thêm (email)->future mapping nếu muốn
                # simpler: recompute by index using position in futures list
                # find index:
                try:
                    f_index = futures.index(fut)
                except ValueError:
                    f_index = None

                # Determine sender_email for log display: use mapping by index if possible
                sender_email_display = None
                if f_index is not None and f_index < len(SENDER_ACCOUNTS):
                    sender_email_display = SENDER_ACCOUNTS[f_index][0]
                else:
                    # fallback: unknown
                    sender_email_display = "unknown_sender"

                if ok:
                    overall_success += 1
                    safe_print(GREEN + f"[✓] {mask_email(sender_email_display)} -> {receiver} | Lần vòng {round_idx+1} | Tiêu đề ({subject})" + RESET)
                else:
                    overall_fail += 1
                    safe_print(RED + f"[X] {mask_email(sender_email_display)} -> {receiver} | Lỗi: {err}" + RESET)
                    with LOG_LOCK:
                        error_logs.append(f"Round {round_idx+1} | {sender_email_display} -> {receiver} | ERR: {err}")

        # chờ giữa các vòng nếu còn vòng tiếp
        if round_idx != total_rounds - 1:
            safe_print(CYAN + f"⏳ Đã hoàn tất vòng {round_idx+1}. Đợi {delay}s trước vòng tiếp theo..." + RESET)
            time.sleep(delay)

    safe_print(CYAN + f"\nHoàn tất toàn bộ: ✅ {overall_success} thành công | ❌ {overall_fail} thất bại" + RESET)

    # ghi log lỗi nếu có
    if error_logs:
        log_name = f"toky_v6_errors_{int(time.time())}.log"
        try:
            with open(log_name, "w", encoding="utf-8") as f:
                f.write("\n".join(error_logs))
            safe_print(YELLOW + f"Lỗi chi tiết được lưu: {log_name}" + RESET)
        except Exception as e:
            safe_print(RED + f"Không thể ghi log: {e}" + RESET)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        safe_print(RED + "\n⛔ Đã dừng tool bởi người dùng." + RESET)
    except Exception:
        safe_print(RED + "\nLỗi không mong muốn (xem traceback):" + RESET)
        traceback.print_exc()
