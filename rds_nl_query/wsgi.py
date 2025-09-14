import os
from django.core.wsgi import get_wsgi_application

# Use production settings if DEBUG is False, otherwise use development settings
settings_module = 'rds_nl_query.settings_production' if os.getenv('DEBUG', 'False').lower() == 'false' else 'rds_nl_query.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
application = get_wsgi_application()