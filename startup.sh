python manage.py migrate
gunicorn --bind=0.0.0.0 --timeout 60 --max-requests 500 --max-requests-jitter 10  ESIFitbit.wsgi
