web: gunicorn myproject.wsgi:application --log-file -
worker: celery -A myproject worker --loglevel=info
