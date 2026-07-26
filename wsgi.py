# Entry point for the production server (gunicorn wsgi:app).
from quotevault.app import create_app

app = create_app()
