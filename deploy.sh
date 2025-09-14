#!/bin/bash

# Production Deployment Script for RDS Natural Language Query

set -e

echo "🚀 Starting production deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from template..."
    cat > .env << EOF
# Production Environment Variables
DEBUG=False
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=rds_nl_query
DB_USER=postgres
DB_PASSWORD=changeme123
DB_HOST=localhost
DB_PORT=5432

# Security
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False

# Static Files
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles/
EOF
    print_warning "Please update .env file with your actual values before deploying!"
fi

# Create logs directory
mkdir -p logs

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose down || true

# Build and start services
print_status "Building and starting services..."
docker-compose up -d --build

# Wait for database to be ready
print_status "Waiting for database to be ready..."
sleep 10

# Run migrations
print_status "Running database migrations..."
docker-compose exec web python manage.py migrate --settings=rds_nl_query.settings_production

# Create superuser (optional)
print_status "Creating superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | docker-compose exec -T web python manage.py shell --settings=rds_nl_query.settings_production

# Collect static files
print_status "Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput --settings=rds_nl_query.settings_production

# Check health
print_status "Checking application health..."
sleep 5

if curl -f http://localhost/api/connections/ > /dev/null 2>&1; then
    print_status "✅ Application is healthy and running!"
    echo ""
    echo "🌐 Access your application at:"
    echo "   - Frontend: http://localhost/frontend.html"
    echo "   - API: http://localhost/api/"
    echo "   - Admin: http://localhost/admin/ (admin/admin123)"
    echo ""
    echo "📊 Monitor logs with: docker-compose logs -f"
    echo "🛑 Stop with: docker-compose down"
else
    print_error "❌ Application health check failed!"
    print_error "Check logs with: docker-compose logs web"
    exit 1
fi

print_status "🎉 Deployment completed successfully!"
