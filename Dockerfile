FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python deps (FORCE uvicorn install)
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "uvicorn[standard]"

# Copy application
COPY . .

#  Render-required port
EXPOSE 10000

# ONLY PORT CHANGED — app.main:app KEPT
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
