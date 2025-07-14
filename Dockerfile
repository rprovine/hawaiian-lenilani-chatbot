# Backend Dockerfile for Hawaiian LeniLani Chatbot
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements-minimal.txt .
RUN pip install --no-cache-dir -r requirements-minimal.txt
RUN pip install --no-cache-dir email-validator gunicorn

# Copy application code
COPY api_backend/ ./api_backend/
COPY claude_integration/ ./claude_integration/

# Set Python path
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run with gunicorn for production
CMD ["gunicorn", "api_backend.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]