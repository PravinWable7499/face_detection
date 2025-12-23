FROM python:3.10-slim

# ===============================
# System dependencies for OpenCV / TF
# ===============================
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# App setup
# ===============================
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ===============================
# Run FastAPI with Gunicorn
# ===============================
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:10000"]
