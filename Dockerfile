FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "uvicorn[standard]"

# Copy application code
COPY . .

# Render requires port 10000
EXPOSE 10000

# Start FastAPI (main.py is at root)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
