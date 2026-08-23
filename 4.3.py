
    
import os
import subprocess
from urllib.parse import urlparse
import zipfile
from colorama import Fore, Style, init
import shutil
init(autoreset=True)

def banner():
    print(Fore.CYAN + Style.BRIGHT + r"""
████████╗ ██████╗ ██╗  ██╗██╗   ██╗
╚══██╔══╝██╔═══██╗██║ ██╔╝╚██╗ ██╔╝
   ██║   ██║   ██║█████╔╝  ╚████╔╝ 
   ██║   ██║   ██║██╔═██╗   ╚██╔╝  
   ██║   ╚██████╔╝██║  ██╗   ██║   
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
         """ + Fore.GREEN + "TOKY DEV TOOL (Get sâu hơn gần 100%)\n" + Style.RESET_ALL)

def check_httrack():
    """Kiểm tra httrack, nếu chưa có thì tự động cài"""
    if shutil.which("httrack") is None:
        print(Fore.YELLOW + "⚠️ HTTrack chưa cài, đang tiến hành cài đặt...")
        try:
            subprocess.run(["pkg", "install", "httrack", "-y"], check=True)
            print(Fore.GREEN + "✅ Đã cài đặt HTTrack thành công!")
        except Exception as e:
            print(Fore.RED + f"❌ Lỗi khi cài đặt HTTrack: {e}")
            exit(1)
    else:
        print(Fore.GREEN + "✅ HTTrack đã sẵn sàng!")        

def zip_folder(folder_path, zip_name):
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    print(Fore.CYAN + f"📂 Đã nén thành: {zip_name}")

if __name__ == "__main__":
    banner()
    url = input(Fore.YELLOW + "🌐 Nhập link website cần tải full source: " + Fore.WHITE).strip()

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    domain = urlparse(url).netloc.split(":")[0]
    if domain.startswith("www."):
        domain = domain[4:]

    out_folder = f"site_{domain}"
    zip_name = f"fullsrcV2_{domain}_tokydev.zip"

    print(Fore.BLUE + f"⚡ Đang chạy HTTrack để mirror site: {url}")
    subprocess.run(["httrack", url, "-O", out_folder, "+*.{js,css,png,jpg,gif,svg,html,php}"], check=False)

    zip_folder(out_folder, zip_name)
    print(Fore.GREEN + "🎉 Hoàn tất! Vui lòng kiểm tra file.")
