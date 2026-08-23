

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
from rich.console import Console
import requests, time, re
from colorama import Fore
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel
import os, re, io, time, json, random, urllib.parse, csv, datetime, certifi, pycurl
console = Console()
init(autoreset=True)

RESULTS_CSV = "ktoollink4m_results.csv"
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
{Fore.CYAN}Icon: 🔗  |  Tool: PYBASS Link4m AUTO V2
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

UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
]
BASE_HEADERS = {
    "Accept": "*/*",
    "User-Agent": random.choice(UA_LIST),
    "Connection": "keep-alive",
}
# ---------- Helpers ----------
def disable_env_proxy():
    for var in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY"]:
        os.environ.pop(var, None)
disable_env_proxy()

# ==================== PY CURL WRAPPER ====================
class CurlSecure:
    def __init__(self, cookie_file=None, timeout=25):
        self.cookie_file = cookie_file
        
        self.timeout = timeout

    def _setup_base(self, curl: pycurl.Curl, url, headers):
        curl.setopt(pycurl.URL, url.encode("utf-8"))
        curl.setopt(pycurl.USERAGENT, headers.get("User-Agent", random.choice(UA_LIST)))
        curl.setopt(pycurl.CONNECTTIMEOUT, 10)
        curl.setopt(pycurl.TIMEOUT, self.timeout)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.MAXREDIRS, 5)
        
        # try block for systems where NOPROXY is not supported
        try:
            curl.setopt(pycurl.NOPROXY, "*")
        except Exception:
            pass
        curl.setopt(pycurl.SSL_VERIFYPEER, 1)
        curl.setopt(pycurl.SSL_VERIFYHOST, 2)
        curl.setopt(pycurl.CAINFO, certifi.where())

        hdr_list = [f"{k}: {v}" for k, v in headers.items()]
        curl.setopt(pycurl.HTTPHEADER, hdr_list)

    def get(self, url, headers=None):
        buf = io.BytesIO()
        curl = pycurl.Curl()
        h = BASE_HEADERS.copy()
        if headers: h.update(headers)
        self._setup_base(curl, url, h)
        curl.setopt(pycurl.WRITEDATA, buf)
        try:
            curl.perform()
            code = curl.getinfo(pycurl.RESPONSE_CODE)
            body = buf.getvalue().decode("utf-8", "ignore")
        finally:
            curl.close()
        if code >= 400:
            raise Exception(f"HTTP {code} on {url}")
        return body

    def post(self, url, data=None, headers=None, json_mode=False):
        buf = io.BytesIO()
        curl = pycurl.Curl()
        h = BASE_HEADERS.copy()
        if headers: h.update(headers)
        self._setup_base(curl, url, h)

        curl.setopt(pycurl.POST, 1)
        if data:
            if json_mode:
                payload = json.dumps(data)
                curl.setopt(pycurl.POSTFIELDS, payload.encode('utf-8'))
                # ensure header present
                if "Content-Type" not in h:
                    h["Content-Type"] = "application/json"
                hdr_list = [f"{k}: {v}" for k, v in h.items()]
                curl.setopt(pycurl.HTTPHEADER, hdr_list)
            else:
                payload = urllib.parse.urlencode({k:v for k,v in data.items() if v is not None})
                curl.setopt(pycurl.POSTFIELDS, payload.encode('utf-8'))

        curl.setopt(pycurl.WRITEDATA, buf)
        try:
            curl.perform()
            code = curl.getinfo(pycurl.RESPONSE_CODE)
            body = buf.getvalue().decode("utf-8", "ignore")
        finally:
            curl.close()
        if code >= 400:
            raise Exception(f"HTTP {code} on {url}")
        return body

# ==================== UTIL ====================
def read_fallback_key():
    if os.path.exists(FALLBACK_KEY_FILE):
        try:
            return open(FALLBACK_KEY_FILE).read().strip() or None
        except:
            return None
    return None

def parse_alias_codes_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    wrapper = soup.find(id="captcha-html-wrapper")
    alias = None
    codes = None
    if wrapper:
        alias = wrapper.get("data-alias") or wrapper.get("data-alias".lower())
        codes = wrapper.get("data-code") or wrapper.get("data-code".lower())
    if not alias:
        m = re.search(r"data-alias=['\"]([^'\"]+)['\"]", html)
        if m: alias = m.group(1)
    if not codes:
        m = re.search(r"data-code=['\"]([^'\"]+)['\"]", html)
        if m: codes = m.group(1)
    return alias, codes

# ==================== ANTICAPTCHA (PYCURL) ====================
def anticaptcha_create_task(curl: CurlSecure, api_key, sitekey, pageurl):
    payload = {
        "key": api_key,
        "method": "userrecaptcha",
        "googlekey": sitekey,
        "pageurl": pageurl,
        "json": 1
    }
    body = curl.post(ANTICAPTCHA_IN, data=payload, json_mode=True)
    j = json.loads(body)
    if j.get("status") == 1:
        return str(j["request"])
    # some providers return "OK|id"
    if isinstance(j, str) and j.startswith("OK|"):
        return j.split("|",1)[1]
    raise Exception(f"anticaptcha.in error: {j}")

def anticaptcha_get_result(curl: CurlSecure, api_key, task_id, wait_sec=3, max_wait=180):
    elapsed = 0
    while elapsed < max_wait:
        params = {"key": api_key, "id": task_id, "json": 1}
        body = curl.get(f"{ANTICAPTCHA_RES}?{urllib.parse.urlencode(params)}")
        try:
            j = json.loads(body)
        except:
            # fallback text
            if body.startswith("OK|"):
                return body.split("|",1)[1]
            raise Exception("anticaptcha.res invalid json")
        if j.get("status") == 1:
            return j["request"]
        if j.get("request") == "CAPCHA_NOT_READY":
            time.sleep(wait_sec)
            elapsed += wait_sec
            continue
        raise Exception(f"anticaptcha.res error: {j}")
    raise Exception("anticaptcha.res timeout")

# ==================== MAIN LOOP / UI ====================
def format_elapsed(start):
    return str(datetime.timedelta(seconds=int(time.time()-start)))

def save_results_csv(rows):
    hdr = ["index","short_url","status","final","sitekey","alias","codes","time_elapsed","note"]
    write_header = not os.path.exists(RESULTS_CSV)
    with open(RESULTS_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(hdr)
        for r in rows:
            w.writerow([r.get(h,"") for h in hdr])

def main():
    
    # choose api key
    console.print(Panel("[1] Dùng api key mặc định\n[2] Nhập api key (lưu lại)", title="API Key", subtitle="Chọn 1 hoặc 2"))
    ch = console.input("[cyan]? Chọn: [/cyan]").strip()
    api_key = None
    if ch == "1":
        api_key = DEFAULT_API_KEY or read_fallback_key()
    elif ch == "2":
        api_key = console.input("[green]Nhập API key: [/green]").strip()
        try:
            with open(FALLBACK_KEY_FILE,"w",encoding="utf-8") as fk:
                fk.write(api_key)
        except:
            pass
    if not api_key:
        console.print("[red]Không có API key — thoát.[/red]")
        return

    console.print(Panel("[bold cyan]Dán các link (mỗi link 1 dòng). Nhập dòng trống để bắt đầu.", title="Links"))
    links = []
    while True:
        l = console.input("> ").strip()
        if not l:
            break
        links.append(l)
    if not links:
        console.print("[red]Không có link nào. Thoát.[/red]")
        return

    curl = CurlSecure()
    start_all = time.time()
    results = []

    # prepare dynamic table
    table = Table(title="Kết quả (live)", box=box.ROUNDED, expand=True)
    table.add_column("#", style="bold white", width=4, justify="right")
    table.add_column("Link", style="cyan", overflow="fold")
    table.add_column("Sitekey", style="magenta")
    table.add_column("Alias", style="yellow")
    table.add_column("Status", style="bold")
    table.add_column("Time", style="green")
    table.add_column("Note", style="dim")

    # progress
    with Progress(
        SpinnerColumn(spinner_name="dots2"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        transient=False,
    ) as progress:
        task = progress.add_task("[cyan]Xử lý links...", total=len(links))
        # live display: combine table + summary
        with Live(console=console, refresh_per_second=4) as live:
            for idx, short_url in enumerate(links, start=1):
                start = time.time()
                status_text = "[yellow]⏳ Pending"
                sitekey = ""
                alias = ""
                codes = ""
                final = ""
                note = ""
                try:
                    # fetch page
                    page_html = curl.get(short_url)
                    alias, codes = parse_alias_codes_from_html(page_html)
                    status_text = "[blue]🔍 Parsed"
                    # call get-advertise
                    body = curl.post(GET_ADVERTISE, data={"alias": alias or "", "codes": codes or ""})
                    j = json.loads(body)
                    if not j.get("success"):
                        raise Exception(f"get-advertise fail: {j}")
                    html = j.get("html","")
                    m = re.search(r'data-sitekey=["\']([^"\']+)["\']', html)
                    if not m:
                        raise Exception("Không tìm thấy sitekey")
                    sitekey = m.group(1)
                    status_text = "[cyan]🧩 Got sitekey"

                    # anticaptcha create task
                    task_id = anticaptcha_create_task(curl, api_key, sitekey, short_url)
                    status_text = "[cyan]🕐 Solving captcha"
                    token = anticaptcha_get_result(curl, api_key, task_id, wait_sec=3, max_wait=180)
                    status_text = "[green]🔓 Solved"

                    # submit to check-captcha
                    resp_body = curl.post(CHECK_CAPTCHA, data={"alias": alias or "", "codes": codes or "", "g-recaptcha-response": token})
                    resp = json.loads(resp_body)
                    if not resp.get("success"):
                        raise Exception(f"check-captcha fail: {resp}")
                    final = resp.get("url") or resp.get("redirect") or resp.get("data") or ""
                    status_text = "[bold green]✅ Success"
                    note = "OK"
                except Exception as e:
                    status_text = f"[bold red]❌ Error"
                    note = str(e)
                elapsed = format_elapsed(start)
                # update table row
                table_rows = []
                # rebuild table each iteration for live update
                table = Table(title="Kết quả (live)", box=box.ROUNDED, expand=True)
                table.add_column("#", style="bold white", width=4, justify="right")
                table.add_column("Link", style="cyan", overflow="fold")
                table.add_column("Sitekey", style="magenta")
                table.add_column("Alias", style="yellow")
                table.add_column("Status", style="bold")
                table.add_column("Time", style="green")
                table.add_column("Note", style="dim")

                # append existing results
                results.append({
                    "index": idx,
                    "short_url": short_url,
                    "status": "SUCCESS" if "Success" in status_text or "Solved" in status_text else "ERROR",
                    "final": final,
                    "sitekey": sitekey,
                    "alias": alias,
                    "codes": codes,
                    "time_elapsed": elapsed,
                    "note": note
                })
                for r in results:
                    st = r["status"]
                    status_display = "[green]✅ Success" if st == "SUCCESS" else "[red]❌ Error"
                    table.add_row(str(r["index"]), r["short_url"], r["sitekey"] or "-", r["alias"] or "-", status_display, r["time_elapsed"], (r["note"][:60] if r["note"] else "-"))

                # summary panels
                succ = sum(1 for x in results if x["status"]=="SUCCESS")
                err = sum(1 for x in results if x["status"]=="ERROR")
                t_elapsed = format_elapsed(start_all)
                summary = Table.grid(expand=True)
                summary.add_column(justify="center")
                summary.add_column(justify="center")
                summary.add_column(justify="center")
                summary.add_row(
                    Panel(f"[bold green]{succ}[/bold green]\n[dim]Thành công", title="✅ Success", width=20),
                    Panel(f"[bold red]{err}[/bold red]\n[dim]Lỗi", title="❌ Error", width=20),
                    Panel(f"[bold]{t_elapsed}[/bold]\n[dim]Tổng thời gian", title="⏱ Tổng", width=28),
                )

                header = Panel.fit(f"[bold yellow]Xử lý Link {idx}/{len(links)}[/bold yellow]\n[cyan]{short_url}[/cyan]", subtitle="link4m pycurl", padding=(1,2))
                live.update(Align.center(Columns([header, summary])))
                # below header show table
                live.update(Align.center(table))
                progress.advance(task)
                time.sleep(1)  # small gap for UI fluidity

    # finished
    console.rule("[bold magenta]KẾT THÚC")
    succ = sum(1 for x in results if x["status"]=="SUCCESS")
    err = sum(1 for x in results if x["status"]=="ERROR")
    console.print(f"[green]Thành công:[/green] {succ}  Link: {final}  [red]Lỗi:[/red] {err}\n[cyan]Kết quả được lưu vào:[/cyan] {RESULTS_CSV}")

    # save CSV
    save_results_csv(results)
    console.print("[bold]🎯 Hoàn tất.\n", style="green")

if __name__ == "__main__":
    main()