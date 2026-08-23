# ──────────────────────────────────────────────────────────────────────
# KTOOL NEON v3.1 - Premium Multi-Tool Suite (Banner Fix - Clean Neon)
# Author: TOKY | Zalo: 0779747160 | Youtube: KTool
# ──────────────────────────────────────────────────────────────────────

import os
import sys
import time
import json
import base64
import random
import string
import requests
import socket
import urllib.parse
import platform
import hashlib
import ctypes
from time import sleep
from datetime import datetime, timedelta
from io import BytesIO
from OpenSSL import SSL

try:
    import psutil
except ImportError:
    os.system(f"{sys.executable} -m pip install psutil >/dev/null 2>&1")
    import psutil

try:
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
except Exception:
    os.system(f"{sys.executable} -m pip install pystyle pyfiglet rich colorama requests pyOpenSSL >/dev/null 2>&1")
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

# ─── ANTI DEBUG ──────────────────────────────────────────────────────
def anti_debug():
    if hasattr(sys, "gettrace") and sys.gettrace() is not None:
        sys.exit(1)
    try:
        with open("/proc/self/status") as f:
            if "TracerPid:\t0" not in f.read():
                sys.exit(1)
    except:
        pass

def anti_pythonpath():
    if "PYTHONPATH" in os.environ:
        sys.exit(1)
    sitecustomize_path = os.path.join(sys.prefix, "lib", "site-packages", "sitecustomize.py")
    if os.path.exists(sitecustomize_path):
        sys.exit(1)

class URLAntiDebug:
    def __init__(self):
        self.blacklisted_processes = [
            "wireshark", "fiddler", "charles", "burpsuite", "mitmproxy", 
            "mitmdump", "httptoolkit", "proxyman", "tcpdump", "tshark",
            "httpdebugger", "httpanalyzer", "packetsender"
        ]
        self.blacklisted_ports = [8080, 8081, 8888, 9090, 8000, 8008, 1337, 1338]

    def execute_protection(self):
        checks = [
            self._check_network_monitoring,
            self._check_http_debugging,
            self._check_packet_capture,
            self._check_mitm_tools,
            self._check_system_proxy,
            self._check_suspicious_ports,
            self._check_ssl_interception,
            self._check_process_list,
            self._check_parent_process,
            self._check_injected_libraries,
            self._check_debugger_present,
            self._check_python_debug,
            self._check_environment_vars,
            self._check_process_timing,
            self._check_runtime_timing,
            self._check_virtual_machine,
            self._check_sandbox_environment,
            self._check_remote_desktop,
            self._check_antivirus_presence
        ]
        
        for i, check in enumerate(checks, 1):
            try:
                if check():
                    self._security_breach_detected(f"Security check #{i} failed")
                    return False
                time.sleep(0.01)
            except:
                continue
        console.print("[green]✓ Security check passed[/green]")
        return True

    def _check_network_monitoring(self):
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() in self.blacklisted_processes:
                    return True
            return False
        except:
            return False

    def _check_http_debugging(self):
        http_tools = ["fiddler", "charles", "mitmproxy", "httptoolkit", "burpsuite"]
        try:
            for proc in psutil.process_iter(['name']):
                if any(tool in proc.info['name'].lower() for tool in http_tools):
                    return True
            return False
        except:
            return False

    def _check_packet_capture(self):
        packet_tools = ["wireshark", "tcpdump", "tshark", "dumpcap"]
        try:
            for proc in psutil.process_iter(['name']):
                if any(tool in proc.info['name'].lower() for tool in packet_tools):
                    return True
            return False
        except:
            return False

    def _check_mitm_tools(self):
        mitm_tools = ["mitmproxy", "mitmdump", "httptoolkit", "burpsuite"]
        try:
            for proc in psutil.process_iter(['name']):
                if any(tool in proc.info['name'].lower() for tool in mitm_tools):
                    return True
            return False
        except:
            return False

    def _check_system_proxy(self):
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
        return any(os.environ.get(var) for var in proxy_vars)

    def _check_suspicious_ports(self):
        try:
            for conn in psutil.net_connections():
                if conn.status == 'LISTEN' and conn.laddr.port in self.blacklisted_ports:
                    return True
            return False
        except:
            return False

    def _check_ssl_interception(self):
        cert_vars = ['SSL_CERT_FILE', 'REQUESTS_CA_BUNDLE']
        return any(os.environ.get(var) for var in cert_vars)

    def _check_process_list(self):
        try:
            for proc in psutil.process_iter(['name']):
                if any(black in proc.info['name'].lower() for black in self.blacklisted_processes):
                    return True
            return False
        except:
            return False

    def _check_parent_process(self):
        try:
            parent = psutil.Process(os.getppid())
            return any(proc in parent.name().lower() for proc in self.blacklisted_processes)
        except:
            return False

    def _check_injected_libraries(self):
        try:
            proc = psutil.Process()
            maps = [m.path.lower() for m in proc.memory_maps() if m.path]
            susp = ["frida", "xposed", "substrate", "hook", "inject"]
            return any(any(s in path for s in susp) for path in maps)
        except:
            return False

    def _check_debugger_present(self):
        try:
            if hasattr(ctypes, 'windll'):
                return ctypes.windll.kernel32.IsDebuggerPresent()
            return False
        except:
            return False

    def _check_python_debug(self):
        return hasattr(sys, 'gettrace') and sys.gettrace() is not None

    def _check_environment_vars(self):
        debug_vars = ['DEBUG', 'PYTHONDEBUG', 'TRACE', 'PROFILE']
        return any(os.environ.get(v) for v in debug_vars)

    def _check_process_timing(self):
        try:
            start = time.time()
            sum(i*i for i in range(1000))
            dt = time.time() - start
            return dt < 0.0001 or dt > 0.1
        except:
            return False

    def _check_runtime_timing(self):
        try:
            start = time.perf_counter()
            for i in range(50):
                hashlib.md5(str(i).encode()).hexdigest()
            dt = time.perf_counter() - start
            return dt > 0.05
        except:
            return False

    def _check_virtual_machine(self):
        vm_proc = ["vbox", "vmware", "virtualbox", "qemu"]
        vm_ind = ["vbox", "vmware", "virtual", "qemu"]
        try:
            for p in psutil.process_iter(['name']):
                if any(v in p.info['name'].lower() for v in vm_proc):
                    return True
            return any(v in platform.system().lower() for v in vm_ind)
        except:
            return False

    def _check_sandbox_environment(self):
        try:
            u = os.getenv('USERNAME', '').lower()
            c = os.getenv('COMPUTERNAME', '').lower()
            sand = ["sandbox", "test", "analysis", "malware"]
            return any(s in u + c for s in sand)
        except:
            return False

    def _check_remote_desktop(self):
        rdp = ["mstsc", "rdp", "vnc", "teamviewer"]
        try:
            for p in psutil.process_iter(['name']):
                if any(r in p.info['name'].lower() for r in rdp):
                    return True
            return False
        except:
            return False

    def _check_antivirus_presence(self):
        av = ["avast", "avg", "bitdefender", "kaspersky", "norton"]
        try:
            for p in psutil.process_iter(['name']):
                if any(a in p.info['name'].lower() for a in av):
                    return True
            return False
        except:
            return False

    def _security_breach_detected(self, msg):
        console.print(f"[red]🚨 SECURITY BREACH: {msg}[/red]")
        os._exit(1)

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
    
    # Font ổn định nhất trên hầu hết terminal: slant hoặc standard
    try:
        fig = Figlet(font='slant', width=100)
        art = fig.renderText("KTOOL")
    except:
        fig = Figlet(font='standard', width=100)
        art = fig.renderText("KTOOL")

    # Gradient ngang đơn giản, ổn định hơn (rainbow hoặc red_to_purple)
    colored_art = Colorate.Horizontal(Colors.red_to_purple, art)

    console.print(Center.XCenter(colored_art))

    # Panel thông tin
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