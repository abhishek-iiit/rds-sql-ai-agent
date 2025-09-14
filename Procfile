web: gunicorn rds_nl_query.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
release: python manage.py migrate --settings=rds_nl_query.settings_production
