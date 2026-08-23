# ──────────────────────────────────────────────────────────────────────
# KTOOL NEON v3.1 - Premium Multi-Tool Suite (Fixed for Python 3.12+ & Android)
# Author: TOKY | Zalo: 0779747160 | Youtube: KTool
# Fixed by: Gemini (Optimized for Android Chaquopy & Termux)
# ──────────────────────────────────────────────────────────────────────

import os
import sys
import time
import json
import base64
import random
import string
import socket
import urllib.parse
import platform
import hashlib
import ctypes
from time import sleep
from datetime import datetime, timedelta
from io import BytesIO

# Import trực tiếp. Trong Android (Chaquopy), các thư viện này khai báo trong build.gradle
# Trong PC/Termux, cần cài đặt trước qua lệnh: pip install psutil pystyle pyfiglet rich colorama requests pyOpenSSL
import psutil
import requests
from OpenSSL import SSL
from pystyle import Colors, Colorate, Center, System
from pyfiglet import Figlet
from rich.console import Console as RichConsole
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.layout import Layout
from rich.align import Align
from rich.box import DOUBLE
from rich.table import Table
from colorama import init as colorama_init

colorama_init(autoreset=True)
console = RichConsole()

# ─── NEON COLOR THEME ────────────────────────────────────────────────
NEON_MAGENTA = "[bold magenta]"
NEON_CYAN    = "[bold cyan]"
NEON_PURPLE  = "[bold purple]"
WHITE_BOLD   = "[bold white]"
DIM          = "[dim]"

THANH_XAU    = f"{NEON_MAGENTA}◆ {NEON_CYAN}[KTOOL NEON] {NEON_MAGENTA}◆"

# ─── ANTI DEBUG (ĐÃ ĐƯỢC BYPASS ĐỂ KHÔNG BỊ CRASH TRÊN ANDROID) ────────
def anti_debug():
    # Vô hiệu hóa để không gây crash app Android
    pass

def anti_pythonpath():
    # Vô hiệu hóa vì Chaquopy trên Android sử dụng cơ chế sitecustomize riêng
    pass

class URLAntiDebug:
    def __init__(self):
        self.blacklisted_processes = []
        self.blacklisted_ports = []

    def execute_protection(self):
        # Bỏ qua các bài test tốc độ CPU và process vì trên chip Mobile sẽ luôn bị nhận diện sai (False Positive)
        # và làm tự động thoát App.
        console.print("[green]✓ Security check passed (Bypassed for Android/Python 3.12)[/green]")
        return True

# ─── HELPERS ─────────────────────────────────────────────────────────
def encrypt_data(plain_text: str) -> str:
    try:
        return base64.b64encode(plain_text.encode('utf-8')).decode('utf-8')
    except:
        return ""

def decrypt_data(cipher_text: str) -> str:
    try:
        return base64.b64decode(cipher_text.encode('utf-8')).decode('utf-8')
    except:
        return ""

def check_internet_connection(timeout=5):
    try:
        requests.get("https://google.com/", timeout=timeout)
        return True
    except:
        return False

# ─── OpenSSLClient ───────────────────────────────────────────────────
class OpenSSLClient:
    def __init__(self, verify=False, timeout=30, max_retry=15):
        self.verify = verify
        self.timeout = timeout
        self.max_retry = max_retry
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/108 Safari/537.36"

    def _create_context(self):
        ctx = SSL.Context(SSL.TLS_CLIENT_METHOD)
        if not self.verify:
            ctx.set_verify(SSL.VERIFY_NONE, lambda *x: True)
        return ctx

    def _recv_all(self, conn):
        data = b""
        conn.settimeout(self.timeout)
        while True:
            try:
                chunk = conn.recv(8192)
                if not chunk: break
                data += chunk
            except SSL.WantReadError:
                time.sleep(0.05)
                continue
            except:
                break
        return data

    def request(self, method, url, headers=None, data=None):
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname
        port = parsed.port or 443
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query

        req_headers = {
            "Host": host,
            "User-Agent": self.ua,
            "Accept": "*/*",
            "Connection": "close",
        }
        if headers:
            req_headers.update(headers)

        body = b""
        if data:
            if isinstance(data, dict):
                body = urllib.parse.urlencode(data).encode()
                req_headers["Content-Type"] = "application/x-www-form-urlencoded"
            elif isinstance(data, (bytes, bytearray)):
                body = data
            else:
                body = str(data).encode()
            req_headers["Content-Length"] = str(len(body))

        header_text = [f"{method} {path} HTTP/1.1"] + \
                      [f"{k}: {v}" for k, v in req_headers.items()] + ["", ""]
        raw_req = ("\r\n".join(header_text)).encode() + body

        ctx = self._create_context()
        sock = socket.create_connection((host, port), timeout=self.timeout)
        ssl_conn = SSL.Connection(ctx, sock)
        ssl_conn.set_connect_state()
        ssl_conn.set_tlsext_host_name(host.encode())

        for _ in range(self.max_retry):
            try:
                ssl_conn.do_handshake()
                break
            except SSL.WantReadError:
                time.sleep(0.1)
            except Exception as e:
                ssl_conn.close()
                sock.close()
                raise e
        else:
            ssl_conn.close()
            sock.close()
            raise TimeoutError("LOI MANG")

        ssl_conn.sendall(raw_req)
        resp = self._recv_all(ssl_conn)
        ssl_conn.close()
        sock.close()
        return self._parse_response(resp)

    def _parse_response(self, raw):
        if not raw:
            return ""
        try:
            header_end = raw.index(b"\r\n\r\n")
            head = raw[:header_end].decode("iso-8859-1")
            body = raw[header_end + 4:]
        except:
            return raw.decode("utf-8", errors="ignore")

        headers = {}
        for line in head.split("\r\n")[1:]:
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.lower().strip()] = v.strip()

        if headers.get("transfer-encoding") == "chunked":
            body = self._decode_chunked(body)

        try:
            return body.decode("utf-8", errors="ignore")
        except:
            return body.decode("latin-1", errors="ignore")

    def _decode_chunked(self, b):
        out = b""
        i = 0
        while True:
            j = b.find(b"\r\n", i)
            if j < 0: break
            try:
                size = int(b[i:j].split(b";")[0], 16)
            except:
                break
            if size == 0: break
            i = j + 2
            out += b[i:i+size]
            i += size + 2
        return out

    def get(self, url, headers=None):
        return self.request("GET", url, headers=headers)

    def post(self, url, data=None, headers=None):
        return self.request("POST", url, headers=headers, data=data)

# ─── BANNER NEON MỚI - CLEAN & STABLE ────────────────────────────────
def banner_neon():
    console.clear()
    
    try:
        fig = Figlet(font='slant', width=100)
        art = fig.renderText("KTOOL")
    except:
        fig = Figlet(font='standard', width=100)
        art = fig.renderText("KTOOL")

    colored_art = Colorate.Horizontal(Colors.red_to_purple, art)

    console.print(Center.XCenter(colored_art))

    info_text = Text.assemble(
        ("\n", ""),
        (f"  {NEON_MAGENTA}Admin: TOKY    {NEON_CYAN}•    {NEON_MAGENTA}Zalo: 0779747160\n", ""),
        (f"  {NEON_MAGENTA}Youtube: KTool    {NEON_CYAN}•    {NEON_MAGENTA}Neon v3.1\n", ""),
        (f"  {DIM}Admin rất nghèo, đừng crack nhé!{WHITE_BOLD}\n", "")
    )

    console.print(Align.center(Panel(
        info_text,
        title=f"{NEON_CYAN} KTOOL NEON ",
        border_style="magenta",
        box=DOUBLE,
        padding=(1, 4),
        subtitle="[dim]Multi-Tool 2025[/dim]"
    )))

# ─── LOADING ─────────────────────────────────────────────────────────
def neon_loading(duration=1.2):
    with Progress(
        SpinnerColumn(spinner_name="dots12"),
        TextColumn("{task.description}"),
        BarColumn(finished_style="magenta", pulse_style="cyan"),
        transient=True,
    ) as progress:
        task = progress.add_task(f"{NEON_MAGENTA}Đang khởi động KTOOL...", total=100)
        for _ in range(101):
            progress.update(task, advance=1)
            sleep(duration / 100)
    console.print(Align.center(Text("HOÀN TẤT ── SẴN SÀNG", style="bold magenta")))

# ─── MENU PANEL ──────────────────────────────────────────────────────
def create_neon_panel(title, color, items):
    table = Table(show_header=False, box=None, padding=(0,1), expand=True)
    table.add_column(f"[bold {color}]{title}", justify="left")

    emojis = ["🚀", "🛠️", "📢", "🔧", "💥", "🔒", "🌐", "📧"]
    for i, (code, name) in enumerate(items):
        emoji = emojis[i % len(emojis)]
        table.add_row(f"{NEON_CYAN}[{code}] {emoji} {WHITE_BOLD}{name}")

    return Panel(
        table,
        border_style=color,
        box=DOUBLE,
        title=f" {NEON_MAGENTA}◆ {title} ◆ ",
        title_align="center",
        padding=(1,1),
        expand=True
    )

def show_menu():
    neon_loading()
    banner_neon()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = Text(f"{THANH_XAU}  KTOOL NEON MENU ── {now}", style="bold white")
    console.print(Align.center(header))

    tds_items = [
        ("1.1", "Cày Xu TDS Tiktok"),
        ("1.2", "Cày Xu TDS Instagram"),
        ("1.3", "Tool Golike Instagram"),
        ("1.4", "Cày Xu TDS Facebook"),
        ("1.5", "Tool Golike Tiktok [auto click]"),
        ("1.6", "Tool Golike Tiktok ADB [Tự Động]"),
    ]
    utility_items = [
        ("2.1", "Buff Share Ảo Cookie"),
        ("2.2", "Get Token Facebook (16 loại)"),
        ("2.3", "Lấy ID Bài Viết/FB"),
        ("2.4", "Get Cookie FB bằng TK/MK"),
        ("2.5", "Spam Tin Nhắn Messenger"),
    ]
    spam_items = [
        ("3.1", "Spam SĐT V1"),
        ("3.2", "Spam SĐT V2"),
        ("3.3", "Spam Gmail"),
        ("3.4", "Spam Gmail V2"),
    ]
    other_items = [
        ("4.1", "Buff Key C25tool"),
        ("4.2", "Get Proxy"),
        ("4.3", "Lọc Proxy"),
        ("4.4", "Scan Mail Ảo Lấy Mã"),
        ("4.5", "Buff Tiktok PC"),
        ("4.6", "Reg Nick FB"),
        ("4.7", "Encode V1 by Tokydev"),
        ("4.8", "Encode pymeomeo [V2]"),
        ("4.9", "Get Suộc web [V1]"),
        ("4.10", "Set Suộc web [V2]"),
        ("4.11", "Ddos web [VIP]"),
        ("4.12", "Reg acc garena [ON]"),
        ("4.13", "Buff view tiktok [ON]"),
        ("4.14", "Tool bypass link4m [VIP]"),
    ]

    layout = Layout()
    layout.split_column(Layout(name="content", ratio=1))

    row1 = Layout()
    row1.split_row(
        Layout(create_neon_panel("TDS & GOLIKE", "magenta", tds_items), ratio=1),
        Layout(create_neon_panel("TIỆN ÍCH", "cyan", utility_items), ratio=1),
    )

    row2 = Layout()
    row2.split_row(
        Layout(create_neon_panel("SPAM TOOLS", "red", spam_items), ratio=1),
        Layout(create_neon_panel("TOOL KHÁC", "purple", other_items), ratio=2),
    )

    layout["content"].split_column(row1, row2)

    console.print(layout)

    console.rule(style="dim magenta")
    console.print(Align.center("[bold cyan]Nhập số tool (ví dụ: 1.1) → [/bold cyan]"))

# ─── LINK CODE ───────────────────────────────────────────────────────
link_code = {
    "1.1": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/1.1.py",
    "1.2": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/1.2.py",
    "1.3": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/1.3.py",
    "1.4": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/1.4.py",
    "1.5": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/1.5.py",
    "1.6": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/1.6.py",
    "2.1": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/2.1.py",
    "2.2": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/2.2.py",
    "2.3": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/23.py",
    "2.4": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/2.4.py",
    "2.5": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/2.5.py",
    "3.1": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/3.5.py",
    "3.2": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/3.6.py",
    "3.3": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/4.1.py",
    "3.4": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/4.1.2.py",
    "4.1": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/3.1.py",
    "4.2": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/3.2.py",
    "4.3": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/3.3.py",
    "4.4": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/3.4.py",
    "4.5": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/3.7.py",
    "4.6": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/3.8.py",
    "4.7": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/3.9.py",
    "4.8": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/4.0.py",
    "4.9": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/4.2.py",
    "4.10": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/4.3.py",
    "4.11": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/4.4.py",
    "4.12": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/4.5.py",
    "4.13": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/4.6.py",
    "4.14": "https://raw.githubusercontent.com/khoa1134/KTool/refs/heads/main/4.7.py",
}

def chay_code(ma):
    if ma not in link_code:
        console.print("[bold red]✖ Mã lựa chọn không hợp lệ![/bold red]")
        return

    url = link_code[ma]
    console.print(f"[magenta]Đang tải module từ server...[/magenta]")

    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        console.print("[bold green]Tải thành công ── Đang khởi chạy...[/bold green]")
        sleep(0.7)
        exec(r.text, globals())
    except Exception as e:
        console.print(f"[bold red]Lỗi: {str(e)}[/bold red]")

# ─── MAIN ────────────────────────────────────────────────────────────
def main():
    anti_debug()
    anti_pythonpath()

    if not check_internet_connection():
        console.print("[red]Check mạng Wifi hoặc 4G![/red]")
        sleep(1)
        return

    anti = URLAntiDebug()
    if not anti.execute_protection():
        return

    while True:
        try:
            show_menu()
            choice = input(Colorate.Horizontal(Colors.rainbow, f"{NEON_CYAN}→ Nhập số: ")).strip()
            if not choice:
                continue
            chay_code(choice)
            console.print("\n[magenta]Nhấn Enter để quay lại menu...[/magenta]")
            input()
        except KeyboardInterrupt:
            console.print("\n[bold cyan]Tạm biệt! KTOOL Neon đã tắt.[/bold cyan]")
            sys.exit(0)
        except Exception as ex:
            console.print(f"[red]Lỗi hệ thống: {ex}[/red]")
            sleep(2)

if __name__ == "__main__":
    main()