import requests
import time
import random
import sys
from datetime import datetime, timedelta
import itertools
import threading

# Logo FER
FER_LOGO = """
███████╗███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗
█████╗  █████╗  ██████╔╝
██╔══╝  ██╔══╝  ██╔══██╗
██║     █████║  ██║  ██║
╚═╝     ╚═╝     ╚═╝  ╚═╝
"""

def display_logo():
    print(FER_LOGO)
    print("\n🚀 Selamat datang di NodeGo - Auto Task NodeGo!")
    time.sleep(2)

# Logo NodeGo dengan animasi
LOGO_TEXT = "NodeGo"
CREDITS = "by: github.com/ayakafer"

def animate_logo():
    for frame in itertools.cycle(['🔥', '⚡', '💎', '🚀']):
        sys.stdout.write(f"\r{frame} {LOGO_TEXT} {frame}  {CREDITS}")
        sys.stdout.flush()
        time.sleep(0.2)

def start_animation():
    t = threading.Thread(target=animate_logo, daemon=True)
    t.start()

# Daftar user-agent untuk menghindari deteksi bot
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/133.0.0.0 Safari/537.36",
]

LAST_CHECKIN = None  # Menyimpan waktu terakhir check-in

# Memuat proxy dari file
USE_PROXY = input("Gunakan proxy? (y/n): ").strip().lower() == 'y'
PROXY_LIST = []
if USE_PROXY:
    try:
        with open("proxy.txt", "r") as file:
            PROXY_LIST = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("⚠️ File proxy.txt tidak ditemukan!")
        USE_PROXY = False

def get_ip():
    url = "https://api.bigdatacloud.net/data/client-ip"
    headers = {"user-agent": random.choice(USER_AGENTS)}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("ipString", "Tidak ditemukan")
    except requests.RequestException:
        return "Gagal mendapatkan IP"
    return "Tidak ditemukan"

def get_tokens():
    with open("token.txt", "r") as file:
        return [f"Bearer {line.strip()}" if not line.startswith("Bearer ") else line.strip() for line in file if line.strip()]

def get_proxy():
    return {"http": random.choice(PROXY_LIST), "https": random.choice(PROXY_LIST)} if PROXY_LIST else None

def fetch_user_data(token, proxy):
    url = "https://nodego.ai/api/user/me"
    headers = {"authorization": token, "user-agent": random.choice(USER_AGENTS)}
    response = requests.get(url, headers=headers, proxies=proxy) if proxy else requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

def daily_checkin(token, proxy):
    global LAST_CHECKIN
    if LAST_CHECKIN and datetime.now() - LAST_CHECKIN < timedelta(hours=12):
        return "✅ Sudah check-in hari ini."
    
    url = "https://nodego.ai/api/user/checkin"
    headers = {"authorization": token, "user-agent": random.choice(USER_AGENTS)}
    response = requests.post(url, headers=headers, proxies=proxy) if proxy else requests.post(url, headers=headers)
    
    if response.status_code == 200:
        LAST_CHECKIN = datetime.now()
        return "✅ Check-in berhasil!"
    elif response.status_code == 400:
        return "✅ Sudah check-in hari ini."
    return "❌ Check-in gagal."

def send_ping(token, proxy):
    url = "https://nodego.ai/api/user/nodes/ping"
    headers = {"authorization": token, "user-agent": random.choice(USER_AGENTS)}
    payload = {"type": "extension"}
    response = requests.post(url, headers=headers, json=payload, proxies=proxy) if proxy else requests.post(url, headers=headers, json=payload)
    return "✅ Ping berhasil!" if response.status_code == 201 else f"⚠️ Ping gagal! Status: {response.status_code}"

def process_account(token, index):
    proxy = get_proxy() if USE_PROXY else None
    user_data = fetch_user_data(token, proxy)
    if not user_data or "metadata" not in user_data:
        print(f"⚠️ Token #{index + 1} tidak valid atau tidak bisa mendapatkan data.")
        return
    
    email = user_data["metadata"].get("email", "Tidak ditemukan")
    nodes = user_data["metadata"].get("nodes", [])
    today_point = sum(node.get("todayPoint", 0) for node in nodes)
    total_point = sum(node.get("totalPoint", 0) for node in nodes)
    
    print(f"\n💠 Token #{index + 1}:")
    print(f"📩 Email: {email}")
    print(f"📊 Today Point: {today_point}")
    print(f"💰 Total Point: {total_point}")
    
    print(daily_checkin(token, proxy))
    
    delay_before_ping = random.randint(40, 45)
    print(f"⏳ Menunggu {delay_before_ping} detik sebelum ping...")
    time.sleep(delay_before_ping)
    
    print(send_ping(token, proxy))
    
    delay_between_accounts = random.randint(5, 10)
    print(f"⏳ Menunggu {delay_between_accounts} detik sebelum akun berikutnya...")
    time.sleep(delay_between_accounts)

if __name__ == "__main__":
    display_logo()
    start_animation()
    
    while True:
        ip_address = get_ip()
        print(f"🌐 IP Publik: {ip_address}\n")
        
        tokens = get_tokens()
        for index, token in enumerate(tokens):
            process_account(token, index)
        
        print("🔄 Menunggu 10 detik sebelum mengulang...")
        time.sleep(10)