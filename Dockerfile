FROM python:3.10-slim

WORKDIR /app

COPY . /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx ffmpeg && \
    pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
