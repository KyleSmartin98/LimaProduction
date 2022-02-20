web: gunicorn mysite.wsgi --log-file -
worker: celery -A mysite.worker --beat
CMD gunicorn --timeout 1000 --workers 1 --threads 4 --log-level debug --bind 0.0.0.0:8000 app:app
