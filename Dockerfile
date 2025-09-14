FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create logs directory
RUN mkdir -p /app/logs

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Collect static files
RUN python manage.py collectstatic --noinput --settings=rds_nl_query.settings_production

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/connections/ || exit 1

# Production command with proper settings
CMD ["gunicorn", "rds_nl_query.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "--keep-alive", "2"]