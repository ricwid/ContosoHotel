cd /app
gunicorn --bind=0.0.0.0 --workers=4 startup:app --timeout 180
