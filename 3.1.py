
    
import requests
import os
import time
import json

KEY_FILE = "saved_key.txt"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print('''\033[1;35m
╔════════════════════════════════════════════╗
║                                            ║
║   ████████╗ ██████╗ ██╗  ██╗██╗   ██╗       ║
║   ╚══██╔══╝██╔═══██╗██║ ██╔╝╚██╗ ██╔╝       ║
║      ██║   ██║   ██║█████╔╝  ╚████╔╝        ║
║      ██║   ██║   ██║██╔═██╗   ╚██╔╝         ║
║      ██║   ╚██████╔╝██║  ██╗   ██║          ║
║      ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝          ║
║                                            ║
╚════════════════════════════════════════════╝
\033[0m''')

def info():
    print("\033[1;33m[-] Admin : Tokydev x anhkhoaa.")
    print("[-] Tool buff key c25, mã gán key : C2589011")
    print("[-] Dùng key trực tiếp từ mã gán key không cần vượt link.\033[0m\n")

def get_real_ip():
    try:
        return requests.get("https://api.ipify.org").text.strip()
    except:
        return None

def get_key(code_key):
    try:
        ip = get_real_ip()
        if not ip:
            print("\033[1;31m[X] Không thể lấy IP thiết bị. Kiểm tra kết nối mạng.\033[0m")
            return

        print(f"\033[1;36m[~] IP của bạn: {ip}\033[0m")

        url = "https://vpsvps112024.c25tool.net/src/keyfree.php"
        res = requests.get(url)
        data = json.loads(res.text)

        if data.get("ip") != ip:
            print("\033[1;31m[X] IP không trùng với IP hệ thống! Bạn đã đổi WiFi?\033[0m")
            print(f"↳ IP hệ thống yêu cầu: {data.get('ip')}")
            return

        link4m = data.get("link", "").replace("\\/", "/")
        print(f"\033[1;32m[✓] Link phù hợp: {link4m}\033[0m")
        time.sleep(1)

        if code_key in data:
            key = data[code_key]
            print(f"\033[1;32m[✓] Key của bạn : {key}")
            print(f"[✓] Mã gán key của bạn : {code_key}")
            print("\033[1;36m[~] Lưu ý : hãy giữ lại mã gán key của bạn để tiếp tục dùng để get key.\033[0m\n")
        else:
            print("\033[1;31m[X] Không tìm thấy mã gán key trong dữ liệu!\033[0m")

    except Exception as e:
        print(f"\033[1;31m[X] Lỗi: {e}\033[0m")

def save_key_to_file(code_key):
    with open(KEY_FILE, "w") as f:
        f.write(code_key)

def load_saved_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            return f.read().strip()
    return None

def ask_for_key():
    while True:
        code_key = input("\033[1;34m[+] Nhập mã được gán key : \033[0m").strip()
        if not code_key.startswith("C25"):
            print("\033[1;31m[X] Mã phải bắt đầu bằng C25\033[0m")
            time.sleep(2)
            continue
        return code_key

def tim_ma_gan_key():
    clear()
    banner()
    print("\033[1;36m[~] Cách để lấy mã gán key để sài mãi mãi:")
    print("↳ Bạn chỉ cần qua tool C25 để lấy link4m và vượt để lấy key.")
    print("↳ Sau khi có key link4m, hãy dán vào ô bên dưới để check ra mã gán key.")
    print("↳ Hãy giữ mã này cẩn thận vì nó sẽ giúp bạn lấy key mãi mãi. \033[0m\n")

    nhap_key = input("\033[1;34m[+] Nhập key đã vượt : \033[0m").strip()

    try:
        ip = get_real_ip()
        if not ip:
            print("\033[1;31m[X] Không thể lấy IP thiết bị. Kiểm tra mạng.\033[0m")
            return

        url = "https://vpsvps112024.c25tool.net/src/keyfree.php"
        res = requests.get(url)
        data = json.loads(res.text)

        for code, key in data.items():
            if key == nhap_key:
                print("\033[1;32m[✓] Key hợp lệ!")
                print(f"[~] Đây là mã gán key của bạn : {code}\033[0m")
                break
        else:
            print("\033[1;31m[X] Không tìm thấy mã gán key tương ứng!\033[0m")

    except Exception as e:
        print(f"\033[1;31m[X] Lỗi: {e}\033[0m")

    input("\n\033[1;33m[0] Nhập 0 để trở lại menu chính...\033[0m")

def main():
    while True:
        clear()
        banner()
        info()

        saved_key = load_saved_key()

        if saved_key:
            print(f"\033[1;36m[~] Mã gán key của bạn : {saved_key}")
            print("[1] Để dùng mã hiện tại")
            print("[2] Để dùng mã mới")
            print("[3] Để lấy mã gán key từ key\033[0m")
            lua_chon = input("\n\033[1;34m[~] Nhập lựa chọn : \033[0m").strip()

            if lua_chon == "1":
                code_key = saved_key
                get_key(code_key)
                break
            elif lua_chon == "2":
                code_key = ask_for_key()
                save_key_to_file(code_key)
                get_key(code_key)
                break
            elif lua_chon == "3":
                tim_ma_gan_key()
            else:
                print("\033[1;31m[X] Lựa chọn không hợp lệ.\033[0m")
                time.sleep(2)
        else:
            print("[1] Nhập mã gán key")
            print("[3] Để lấy mã gán key từ key \033[0m")
            lua_chon = input("\n\033[1;34m[~] Nhập lựa chọn : \033[0m").strip()
            if lua_chon == "1":
                code_key = ask_for_key()
                save_key_to_file(code_key)
                get_key(code_key)
                break
            elif lua_chon == "3":
                tim_ma_gan_key()
            else:
                print("\033[1;31m[X] Lựa chọn không hợp lệ.\033[0m")
                time.sleep(2)

if __name__ == "__main__":
    main()
    