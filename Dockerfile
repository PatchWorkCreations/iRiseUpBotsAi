# Start with your existing base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=myproject.settings
ENV PYTHONUNBUFFERED=1

# Optional: If you have any environment variables for database configuration, set them here

# Run migrations without collectstatic
RUN python manage.py migrate

# Start Django using gunicorn (or your preferred WSGI server)
CMD gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
