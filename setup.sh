#!/bin/bash

echo "Setting up RDS Natural Language Query System..."

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please edit it with your credentials."
fi

# Run Django migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "Creating superuser (optional)..."
python manage.py createsuperuser --noinput --username admin --email admin@admin.com || true

echo "Setup complete!"
echo ""
echo "To start the server:"
echo "1. Activate virtual environment: source .venv/bin/activate"
echo "2. Edit .env file with your credentials"
echo "3. Run server: python manage.py runserver"
echo "4. Open Run frontend serer using python3 -m http.server 3000"
echo "5. http://localhost:3000/frontend.html"