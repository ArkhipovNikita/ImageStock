web: gunicorn ImageStock.wsgi
worker: celery -A settings.celery worker -l info
beat: celery -A settings.celery beat -l info