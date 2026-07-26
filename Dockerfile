FROM python:3.12-slim
WORKDIR /app
# copy dependency list first so the install layer is cached
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# copy the app code
COPY quotevault ./quotevault
COPY wsgi.py .
# create and switch to a non-root user
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
# gunicorn is a production WSGI server; wsgi:app is the app object in wsgi.py
CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app"]
