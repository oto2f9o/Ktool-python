
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bypass4m.py - PYBASS Link4m AUTO (TOKY)
Flow:
 - Tự parse alias/codes từ URL
 - Bước 1: Gửi captcha info -> anticaptcha.top (POST /in.php JSON)
 - Bước 2: Poll kết quả -> anticaptcha.top (GET /res.php JSON)
 - Gửi token lên /links/check-captcha để lấy link đích
Menu API key:
 [1] Dùng API key có sẵn trong file (DEFAULT_API_KEY var)
 [2] Nhập API key thủ công
 Fallback: nếu key mặc định rỗng -> đọc từ apikeycaptcha_ktool.txt
"""
import os, json, re, time, requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init(autoreset=True)

# ---------------- Banner TOKY (the exact one you asked) ----------------
banner = f"""
{Fore.RED} ╔════════════════════════════════════════════════════╗
{Fore.YELLOW}║   ████████╗ ██████╗ ██╗  ██╗██╗   ██╗               ║
{Fore.GREEN}║   ╚══██╔══╝██╔═══██╗██║ ██╔╝╚██╗ ██╔╝               ║ {Fore.CYAN}PYBASS (TOKY)
{Fore.BLUE}║      ██║   ██║   ██║█████╔╝  ╚████╔╝                ║
{Fore.MAGENTA}║      ██║   ██║   ██║█████╔╝  ╚████╔╝                ║
{Fore.YELLOW}║      ██║   ██║   ██║██╔═██╗   ╚██╔╝                 ║
{Fore.MAGENTA}║      ██║   ╚██████╔╝██║  ██╗   ██║                  ║
{Fore.BLUE}║      ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝                  ║
{Fore.GREEN}║                                                    ║
{Fore.RED}╚════════════════════════════════════════════════════╝
{Fore.CYAN}Icon: 🔗  |  Tool: PYBASS Link4m AUTO V1
{Fore.CYAN}Icon: 👑  |  Admin Tool : Toky là KTool
{Fore.CYAN}Icon: ▶️  |  Youtube : @ktool_toky
{Fore.CYAN}Icon: 🎧  |  Tiktok : @ktool_182
{Fore.CYAN}Icon: 💵  |  donate qua : stk : 0793667866 mbbank
{Style.RESET_ALL}
"""
print(banner)

# --------- Config / Endpoints ----------
GET_ADVERTISE = "https://link4m.com/api/campaign/get-advertise"
CHECK_CAPTCHA  = "https://link4m.com/links/check-captcha"
ANTICAPTCHA_IN = "https://anticaptcha.top/in.php"
ANTICAPTCHA_RES= "https://anticaptcha.top/res.php"

# Default API key in-file (PUT YOUR DEFAULT KEY HERE if you want)
DEFAULT_API_KEY = "4dcc5fce98412ddd24cf0dde4067e038"  # <-- nếu muốn đặt mặc định, điền ở đây

FALLBACK_KEY_FILE = "apikeycaptcha_ktool.txt"
HEADERS = {"User-Agent":"Mozilla/5.0", "Accept":"*/*", "X-Requested-With":"XMLHttpRequest"}

# ---------- Helpers ----------
def read_fallback_key():
    if os.path.exists(FALLBACK_KEY_FILE):
        try:
            with open(FALLBACK_KEY_FILE,"r",encoding="utf-8") as f:
                k = f.read().strip()
                return k if k else None
        except:
            return None
    return None

def parse_alias_codes_from_page(url, session):
    """GET short url and extract alias & codes from element #captcha-html-wrapper data attrs"""
    r = session.get(url, headers=HEADERS, timeout=12)
    r.raise_for_status()
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    wrapper = soup.find(id="captcha-html-wrapper")
    alias = None; codes = None
    if wrapper:
        alias = wrapper.get("data-alias") or wrapper.get("data-alias".lower())
        codes = wrapper.get("data-code") or wrapper.get("data-code".lower()) or wrapper.get("data-code".upper())
    # fallback: search scripts for alias/codes
    if not alias:
        m = re.search(r"data-alias=['\"]([^'\"]+)['\"]", html)
        if m: alias = m.group(1)
    if not codes:
        m = re.search(r"data-code=['\"]([^'\"]+)['\"]", html)
        if m: codes = m.group(1)
    return alias, codes, html

# ---------- Anticaptcha interaction (Step 1 & 2) ----------
def anticaptcha_create_task(api_key, sitekey, pageurl, timeout=20):
    """
    Bước 1: Gửi thông tin captcha tới anticaptcha.top (POST JSON).
    Trả về task_id (string) hoặc raise Exception.
    """
    payload = {
        "key": api_key,
        "method": "userrecaptcha",
        "googlekey": sitekey,
        "pageurl": pageurl,
        "json": 1
    }
    r = requests.post(ANTICAPTCHA_IN, json=payload, timeout=timeout)
    r.raise_for_status()
    try:
        j = r.json()
    except:
        # text form OK|ID
        txt = r.text.strip()
        if txt.startswith("OK|"):
            return txt.split("|",1)[1]
        raise Exception("anticaptcha.in non-json: " + txt[:200])
    if j.get("status") == 1:
        return str(j.get("request"))
    raise Exception("anticaptcha.in error: " + json.dumps(j, ensure_ascii=False))

def anticaptcha_get_result(api_key, task_id, wait_sec=3, max_wait=180):
    """
    Bước 2: Poll để nhận token. Trả về token string.
    """
    elapsed = 0
    while elapsed < max_wait:
        params = {"key": api_key, "id": task_id, "json": 1}
        r = requests.get(ANTICAPTCHA_RES, params=params, timeout=20)
        r.raise_for_status()
        try:
            j = r.json()
        except:
            raise Exception("anticaptcha.res invalid response")
        if j.get("status") == 1:
            return j.get("request")
        if j.get("request") == "CAPCHA_NOT_READY":
            time.sleep(wait_sec)
            elapsed += wait_sec
            continue
        raise Exception("anticaptcha.res error: " + json.dumps(j, ensure_ascii=False))
    raise Exception("anticaptcha.res timeout")

# ---------- Main flow ----------
def main():
    # Menu for API key
    print(Fore.YELLOW + "[1] Dùng api key có sẵn (file python)")
    print(Fore.YELLOW + "[2] Dùng api key tự lấy từ web anticaptcha.top")
    choice = input(Fore.CYAN + "[?] Chọn phương án: ").strip()

    api_key = None
    if choice == "1":
        api_key = DEFAULT_API_KEY or None
        if not api_key:
            api_key = read_fallback_key()
        if not api_key:
            print(Fore.RED + "[!] Không tìm thấy api key có sẵn. vui lòng chọn bước 2")
            return
    elif choice == "2":
        print(Fore.CYAN + "[=] Hướng dẫn: vào anticaptcha.top -> account -> API key. Dán vào bên dưới.")
        api_key = input(Fore.GREEN + "[=] Nhập api key : ").strip()
        if not api_key:
            print(Fore.RED + "[!] Bạn chưa nhập api key.")
            return
        # save entered key to fallback file for reuse
        try:
            with open(FALLBACK_KEY_FILE, "w", encoding="utf-8") as fk:
                fk.write(api_key)
        except:
            pass
    else:
        print(Fore.RED + "[!] Lựa chọn không hợp lệ.")
        return

    # Input short url
    short_url = input(Fore.YELLOW + "[-] Nhập link4m cần bypass : ").strip()
    print(Fore.CYAN + "[~] Đang bypass")

    s = requests.Session()
    try:
        alias, codes, page_html = parse_alias_codes_from_page(short_url, s)
        print(Fore.GREEN + f"[^] Phát hiện alias và code : {alias} / {('present' if codes else 'MISSING')}")
    except Exception as e:
        print(Fore.RED + "[❌] Lỗi khi lấy alias/code:", e)
        return

    # Call get-advertise (to obtain html if needed)
    try:
        headers = HEADERS.copy()
        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        data = {"alias": alias}
        if codes: data["codes"] = codes
        r = s.post(GET_ADVERTISE, headers=headers, data=data, timeout=12)
        r.raise_for_status()
        j = r.json()
        if not j.get("success"):
            print(Fore.RED + "[❌] get-advertise không thành công:" + str(j))
            return
        html = j.get("html","")
    except Exception as e:
        print(Fore.RED + "[❌] Lỗi get-advertise:", e)
        return

    # extract sitekey
    m = re.search(r'data-sitekey=["\']([^"\']+)["\']', html)
    if not m:
        print(Fore.RED + "[❌] Không tìm thấy sitekey trong HTML.")
        return
    sitekey = m.group(1)
    print(Fore.CYAN + f"[~] Found sitekey: {sitekey}")

    # Step 1: create task
    try:
        task_id = anticaptcha_create_task(api_key, sitekey, short_url)
        print(Fore.CYAN + f"[~] Task created id: {task_id}")
    except Exception as e:
        print(Fore.RED + "[❌] Lỗi tạo task anticaptcha:", e)
        return

    # Step 2: poll result
    try:
        token = anticaptcha_get_result(api_key, task_id, wait_sec=3, max_wait=180)
        print(Fore.GREEN + "[✓] Thành công truy cập (captcha solved)")
    except Exception as e:
        print(Fore.RED + "[❌] Lỗi khi lấy token:", e)
        return

    # Submit token to check-captcha
    try:
        headers2 = HEADERS.copy()
        headers2["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        data2 = {"g-recaptcha-response": token}
        # some implementations expect alias/codes as well; include them
        if alias: data2["alias"] = alias
        if codes: data2["codes"] = codes
        r2 = s.post(CHECK_CAPTCHA, headers=headers2, data=data2, timeout=12)
        r2.raise_for_status()
        resp = r2.json()
        if not resp.get("success"):
            print(Fore.RED + "[❌] check-captcha trả về lỗi:", resp)
            return
        final = resp.get("url") or resp.get("redirect") or resp.get("data")
        if not final:
            print(Fore.RED + "[❌] Không thấy link đích trong response:", resp)
            return
        print(Fore.GREEN + "[√] Thành công")
        print(Fore.GREEN + f"[√] Link đã vượt bạn cần : {final}")
    except Exception as e:
        print(Fore.RED + "[❌] Lỗi khi verify token:", e)
        return

if __name__ == "__main__":
    main()
