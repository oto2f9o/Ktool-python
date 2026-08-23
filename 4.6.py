
    

import random, requests, re, threading, time, secrets, os
from hashlib import md5
from time import time as T
import pyfiglet
from rich.console import Console

console = Console()

# =========================
# ====== BANNER TOKY ======
# =========================
os.system("cls" if os.name == "nt" else "clear")

tool_name = "Buff view tiktok"
banner_text = pyfiglet.figlet_format("TOKY", font="slant")
colors = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]

console.print("=" * 60, style="bold white")
for line in banner_text.split("\n"):
    if line.strip():
        color = random.choice(colors)
        console.print(line, style=f"bold {color}")
console.print("=" * 60, style="bold white")
console.print(f"[💥] TOOL: {tool_name}", style="bold magenta")
console.print(f"[🔥] DEV: TOKY", style="bold cyan")
console.print(f"[🌀] Treo Tool để tự chạy sẽ tăng view !\n", style="bold green")
console.print("=" * 60 + "\n", style="bold white")
# =========================

def random_device():
    devices = ["Pixel 6", "Pixel 5", "Samsung Galaxy S21", "Oppo Reno 8", "Xiaomi Mi 11"]
    os_versions = ["12", "13", "14"]
    return random.choice(devices), random.choice(os_versions), random.randint(26, 34)

class Signature:
    def __init__(self, params: str, data: str, cookies: str) -> None:
        self.params = params; self.data = data; self.cookies = cookies
    def hash(self, data: str) -> str: return str(md5(data.encode()).hexdigest())
    def calc_gorgon(self) -> str:
        g = self.hash(self.params)
        g += self.hash(self.data) if self.data else "0"*32
        g += self.hash(self.cookies) if self.cookies else "0"*32
        g += "0"*32
        return g
    def get_value(self): return self.encrypt(self.calc_gorgon())
    def encrypt(self, data: str):
        unix = int(T()); length = 0x14
        key = [0xDF,0x77,0xB9,0x40,0xB9,0x9B,0x84,0x83,0xD1,0xB9,0xCB,0xD1,0xF7,0xC2,0xB9,0x85,0xC3,0xD0,0xFB,0xC3]
        pl = []
        for i in range(0,12,4):
            t = data[8*i:8*(i+1)]
            for j in range(4): pl.append(int(t[j*2:(j+1)*2],16))
        pl.extend([0x0,0x6,0xB,0x1C])
        H = int(hex(unix),16)
        pl += [(H&0xFF000000)>>24,(H&0x00FF0000)>>16,(H&0x0000FF00)>>8,(H&0x000000FF)>>0]
        e = [a^b for a,b in zip(pl,key)]
        for i in range(length):
            C=self.reverse(e[i]);D=e[(i+1)%length];F=self.rbit(C^D);H=((F^0xFFFFFFFF)^length)&0xFF;e[i]=H
        r="".join(self.hex_string(x) for x in e)
        return {"X-Gorgon":"840280416000"+r,"X-Khronos":str(unix)}
    def rbit(self,n):s=bin(n)[2:].zfill(8);return int(s[::-1],2)
    def hex_string(self,n):s=hex(n)[2:];return s if len(s)==2 else "0"+s
    def reverse(self,n):s=self.hex_string(n);return int(s[1:]+s[:1],16)

link = input("Nhập link video TikTok: ")
headers_id = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

try:
    page = requests.get(link, headers=headers_id, timeout=10).text
    m = re.search(r'"video":\{"id":"(\d+)"', page)
    if m:
        video_id = m.group(1)
        console.print(f"[✅] Video ID: {video_id}", style="bold green")
    else:
        console.print("[-] Không tìm thấy ID Video", style="bold red")
        exit(1)
except Exception as e:
    console.print(f"[-] Lỗi lấy ID Video: {e}", style="bold red")
    exit(1)

ua_list = [
    "com.ss.android.ugc.trill/400304 (Linux; U; Android 13; vi_VN; Pixel 6; Build/TQ3A.230805.001; Cronet/TTNetVersion:df66ad56)",
    "com.ss.android.ugc.trill/400304 (Linux; U; Android 12; vi_VN; Samsung Galaxy S21; Build/SP1A.210812.016; Cronet/TTNetVersion:df66ad56)",
    "com.ss.android.ugc.trill/400304 (Linux; U; Android 14; vi_VN; Xiaomi Mi 11; Build/UPB1.230309.014; Cronet/TTNetVersion:df66ad56)"
]

def send_view():
    device_type, os_version, os_api = random_device()
    params = (f"channel=googleplay&aid=1233&app_name=musical_ly&version_code=400304&device_platform=android"
              f"&device_type={device_type.replace(' ', '+')}&os_version={os_version}"
              f"&device_id={random.randint(600000000000000,699999999999999)}&os_api={os_api}&app_language=vi&tz_name=Asia%2FHo_Chi_Minh")
    url = f"https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/?{params}"
    cookies = {"sessionid": secrets.token_hex(8)}

    while True:
        data = {"item_id": video_id, "play_delta": 1, "action_time": int(time.time())}
        sig = Signature(params=params, data=str(data), cookies=str(cookies)).get_value()
        headers = {
            "Host": "api16-core-c-alisg.tiktokv.com",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": random.choice(ua_list),
            "Sdk-Version": "2",
            "Passport-Sdk-Version": "19",
            "X-SS-DP": "1233",
            "X-Khronos": sig["X-Khronos"],
            "X-Gorgon": sig["X-Gorgon"]
        }

        try:
            r = requests.post(url, data=data, headers=headers, cookies=cookies, timeout=10)
            if r.status_code != 200:
                console.print(f"⚠️ Server trả về mã {r.status_code}", style="yellow")
                time.sleep(2)
                continue

            if "application/json" in r.headers.get("Content-Type", "") and r.text.strip():
                try:
                    resp = r.json()
                    console.print(f"✅ Thành Công buff View | 1", style="green")
                except Exception as e:
                    console.print(f"⚠️ JSON lỗi: {e}", style="red")
            else:
                console.print(f"💫Đang Đợi Phản hồi", style="yellow")
        except Exception as e:
            console.print(f"❌ Lỗi: {e}", style="red")
            time.sleep(2)

        time.sleep(random.uniform(0.5, 1.5))

threads = []
for i in range(50):
    t = threading.Thread(target=send_view)
    t.daemon = True
    t.start()
    threads.append(t)

for t in threads:
    t.join()
    