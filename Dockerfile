# syntax=docker/dockerfile:1
FROM python:3.10-slim

# 1) Install system deps for Manim
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango1.0-0 libpangocairo-1.0-0 libcairo2 \
    git ffmpeg \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2) Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copy the rest of your code
COPY . .

# 4) Set env vars for Google auth (you'll mount a service-account key)
ENV GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp-key.json

# 5) Expose Cloud Run port
ENV PORT=8080
EXPOSE 8080

# 6) Launch UVicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
