FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx ffmpeg \
    && pip install --no-cache-dir \
    opencv-python-headless \
    fastapi \
    uvicorn \
    numpy \
    sort

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]