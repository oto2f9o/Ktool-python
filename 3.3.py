
    
import requests
from concurrent.futures import ThreadPoolExecutor
import os
import sys
import time
import colorama
from time import sleep
import random

colorama.init()

# Hàm in chậm từng ký tự
def slow_type(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# Banner
def banner():
    text = '''
\033[1;34m╔════════════════════════════════════════════════════════════════╗
\033[1;34m║\033[1;32m████████╗ ██████╗ ██╗  ██╗██╗   ██╗
\033[1;34m║\033[1;36m╚══██╔══╝██╔═══██╗██║ ██╔╝╚██╗ ██╔╝
\033[1;34m║\033[1;31m   ██║   ██║   ██║█████╔╝  ╚████╔╝
\033[1;34m║\033[1;33m   ██║   ██║   ██║██╔═██╗   ╚██╔╝
\033[1;34m║\033[1;34m   ██║   ╚██████╔╝██║  ██╗   ██║
\033[1;34m║\033[1;34m   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝
\033[1;34m╚════════════════════════════════════════════════════════════════╝
\033[1;34m╠═════════════════════════════════════════════════════════════════
\033[1;32m║➢ Author   :    Tokydev
\033[1;36m║➢ Youtube  :   KTool
\033[1;31m║➣ Zalo     : 0779747160
\033[1;34m╚═════════════════════════════════════════════════════════════════
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
'''
    slow_type(text, delay=0.00)

# Xoá màn hình
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# In thanh tiêu đề
def thanh():
    print("\033[1;37m >>TOOL LỌC PROXY<<")

# Chạy tool
sleep(1)
clear()
banner()
thanh()
slow_type(" ")
sleep(1)

proxy_list = input("\033[1;32m Vui lòng nhập file chứa Proxy: \033[1;33m")
with open(proxy_list, 'r') as file:
    proxy_list = file.read().splitlines()

proxy_count = len(proxy_list)
luu = input("\033[1;31m Vui lòng nhập tệp để lưu Proxy Live: \033[1;37m")

slow_type(f" \033[1;31mFound: \033[1;37m{proxy_count} \033[1;31mproxy in your proxy file")
sleep(1)
slow_type(" \033[1;31mPlease \033[1;37mwait \033[1;31mfor \033[1;37ma \033[1;31msec")
sleep(1)

print(" \033[1;37mStart \033[1;31mrunning \033[1;37mthe \033[1;31mtool\033[1;37m. \033[1;31mPlease \033[1;37mdon't \033[1;31mpress \033[1;37manything")
print("\033[1;37m ———————————————————————————————————————————————")
sleep(1)

# Hàm kiểm tra proxy
def check_proxy(proxy):
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
        if response.status_code in [200, 202, 500, 502, 503, 504]:
            detect_location(proxy)
            with open(luu, 'a') as f:
                f.write(proxy + '\n')
            return True
    except requests.exceptions.RequestException:
        pass

    print(f" \033[1;37m[\033[1;31m+\033[1;37m] {proxy} \033[1;31m• \033[1;37mUnknown/Unknown \033[1;31m• \033[1;31mBAD")
    return False

# Hàm lấy vị trí proxy
def detect_location(proxy):
    ip_address = proxy.split(':')[0]
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                print(f" \033[1;37m[\033[1;31mC25\033[1;37m] {proxy} \033[1;31m• \033[1;37m{data['country']}/{data['city']} \033[1;31m• \033[1;32mLIVE")
            else:
                print(" \033[1;37m[\033[1;31m+\033[1;37m] \033[1;31mFailed to detect location for proxy.")
    except:
        pass

# Hàm xử lý từng proxy
def process_proxy(proxy):
    check_proxy(proxy)

# Chạy đa luồng kiểm tra proxy
num_workers = 200
with ThreadPoolExecutor(max_workers=num_workers) as executor:
    executor.map(process_proxy, proxy_list)

# Hiển thị kết quả
with open(luu, 'r') as f:
    live_count = len(f.readlines())

print(f"\033[1;31m Scanning proxies successfully. Currently on the proxy list \033[1;37m{luu} \033[1;31mhas \033[1;37m{live_count} \033[1;31mproxies-live")
print("\033[1;31m Thanks for using my tool <3")
input(" Press enter to exit!")
exit()
