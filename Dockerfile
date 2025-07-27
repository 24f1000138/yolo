FROM python:3.10-slim

WORKDIR /app

COPY . /app
COPY requirements.txt .


RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    ffmpeg \
    build-essential \
    cmake \
    ninja-build \
    python3-dev \
    libopencv-dev \
    python3-opencv \
 && pip install --no-cache-dir -r requirements.txt \
 && apt-get clean && rm -rf /var/lib/apt/lists/*
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
