web: bash -c "python manage.py migrate && python manage.py createsuperuser --no-input && python manage.py collectstatic --noinput && gunicorn start.wsgi"
