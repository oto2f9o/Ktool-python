
    
import os
import marshal
import zlib
import base64
from pathlib import Path

def encode_stage(code):
    compiled = compile(code, "<string>", "exec")
    marshaled = marshal.dumps(compiled)
    compressed = zlib.compress(marshaled)
    encoded = base64.b64encode(compressed).decode()
    return f"import marshal,zlib,base64;exec(marshal.loads(zlib.decompress(base64.b64decode('{encoded}'))))"

def add_anti_debug(code):
    anti = (
        "import sys\n"
        "if sys.gettrace():\n"
        "    print('Debugger detected!'); exit()\n"
    )
    return anti + code

def c(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def main():
    print(c("══════════════════════════════════════════════════════", "93"))
    print(c("        [TOKY x Anhkhoaa PREMIUM] TOOL ENCODER", "95"))
    print(c("══════════════════════════════════════════════════════", "93"))

    user = input(c("[TOKY PREMIUM]  Nhập tên user của bạn: ", "96"))
    filepath = input(c("[TOKY PREMIUM]  Nhập tên file cần mã hóa: ", "96")).strip()
    layers = input(c("[TOKY PREMIUM]  Số lớp mã hóa (1-1000) số cao đợi lâu: ", "96")).strip()
    anti_debug = input(c("[TOKY PREMIUM]  Chống debug / crack (y/n): ", "96")).strip().lower()
    print("Vui Lòng chờ")

    if not Path(filepath).exists():
        print(c("[!] File không tồn tại.", "91"))
        return

    try:
        layers = int(layers)
        if layers < 1 or layers > 1000:
            print(c("[!] Số lớp phải từ 1 đến 1000.", "91"))
            return
    except:
        print(c("[!] Số lớp không hợp lệ.", "91"))
        return

    code = Path(filepath).read_text()
    if anti_debug == 'y':
        code = add_anti_debug(code)

    code = f"print('Đang vào Tool...')\n" + code

    for _ in range(layers):
        code = encode_stage(code)

    output_file = f"encode_{Path(filepath).stem}.py"
    Path(output_file).write_text(code)

    print()
    print(c("[✓] File đã được mã hóa: ", "92") + output_file)
    print(c("[✓] Người dùng: ", "92") + user)
    print(c("[✓] Hoàn tất mã hóa thành công!", "92"))
    print()

if __name__ == "__main__":
    main()
