web: python backend/manage.py migrate && python backend/manage.py collectstatic --no-input && gunicorn backend.core.wsgi:application --bind 0.0.0.0:$PORT
worker: python -m bot.main
