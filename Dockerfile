FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m myuser && chown -R myuser /app

# Copy and install requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set ownership and permissions
RUN chown -R myuser:myuser /app && \
    chmod -R 755 /app && \
    chmod +x app.py

# Switch to non-root user
USER myuser

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PORT=3000

EXPOSE 3000

CMD ["gunicorn", "--bind", "0.0.0.0:3000", "app:app"] 