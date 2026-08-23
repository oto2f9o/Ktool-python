
    

import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import zipfile
from colorama import Fore, Style, init
from collections import deque

init(autoreset=True)
downloaded = set()
visited_pages = set()

# Banner TOKY
def banner():
    print(Fore.CYAN + Style.BRIGHT + r"""
████████╗ ██████╗ ██╗  ██╗██╗   ██╗
╚══██╔══╝██╔═══██╗██║ ██╔╝╚██╗ ██╔╝
   ██║   ██║   ██║█████╔╝  ╚████╔╝ 
   ██║   ██║   ██║██╔═██╗   ╚██╔╝  
   ██║   ╚██████╔╝██║  ██╗   ██║   
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
         """ + Fore.GREEN + "TOKY DEV TOOL ( Không chắc sẽ crack full 100% )\n" + Style.RESET_ALL)

def download_file(session, url, folder):
    if url in downloaded:
        return None
    downloaded.add(url)

    try:
        r = session.get(url, timeout=10)
        if r.status_code == 200:
            path = urlparse(url).path
            if path.endswith("/") or path == "":
                filename = "index.html"
            else:
                filename = os.path.basename(path)

            dir_path = os.path.join(folder, os.path.dirname(path.lstrip("/")))
            os.makedirs(dir_path, exist_ok=True)

            file_path = os.path.join(dir_path, filename)

            with open(file_path, "wb") as f:
                f.write(r.content)

            print(Fore.GREEN + "✅ Tải:" + Fore.YELLOW, file_path)
            return file_path, r.text, r.headers.get("content-type", "")
    except Exception as e:
        print(Fore.RED + "❌ Lỗi tải:", url, e)
    return None, None, None


def crawl_website(base_url, download_folder="website_src"):
    session = requests.Session()
    domain = urlparse(base_url).netloc

    queue = deque([base_url])

    while queue:
        current_url = queue.popleft()
        if current_url in visited_pages:
            continue
        visited_pages.add(current_url)

        file_path, content, ctype = download_file(session, current_url, download_folder)
        if not content:
            continue

        # Nếu là HTML thì tiếp tục tìm link con
        if "text/html" in ctype:
            soup = BeautifulSoup(content, "html.parser")

            # Tìm tất cả thẻ có link
            tags = {
                "a": "href",
                "link": "href",
                "script": "src",
                "img": "src"
            }

            for tag, attr in tags.items():
                for item in soup.find_all(tag):
                    src = item.get(attr)
                    if src:
                        full_url = urljoin(current_url, src)
                        parsed = urlparse(full_url)

                        # Chỉ tải link cùng domain
                        if parsed.netloc == "" or parsed.netloc == domain:
                            if full_url not in visited_pages and full_url not in queue:
                                queue.append(full_url)

    return download_folder


def zip_folder(folder_path, zip_name):
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    print(Fore.CYAN + f"📂 Đã nén toàn bộ source thành: {zip_name}")


if __name__ == "__main__":
    banner()
    url = input(Fore.YELLOW + "🌐 Nhập link website cần tải full source: " + Fore.WHITE).strip()

    # Nếu chưa có http/https thì tự thêm https://
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    domain = urlparse(url).netloc.split(":")[0]
    if domain.startswith("www."):
        domain = domain[4:]  # bỏ "www."

    folder = f"website_src_{domain}"
    print(Fore.BLUE + f"⚡ Đang Crack toàn bộ website (recursive): {url}")
    result = crawl_website(url, folder)
    if result:
        zip_name = f"fullsrc_{domain}_tokydev.zip"
        zip_folder(result, zip_name)
        print(Fore.GREEN + "🎉 Đã hoàn thành file ! Vui lòng kiểm tra .")
