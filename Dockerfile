FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directories
RUN mkdir -p data/raw data/processed

# Expose port
EXPOSE $PORT

# Run ETL pipeline on startup, then start API
CMD ["sh", "-c", "python scripts/run_pipeline.py && python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT"]
