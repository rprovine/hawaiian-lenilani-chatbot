FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create required directories
RUN mkdir -p logs/leads && \
    chmod -R 755 logs

# Render provides PORT env variable
ENV PORT=8000
EXPOSE ${PORT}

# Use unbuffered output for better logging
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "run_backend.py"]