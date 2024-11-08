# Use a minimal Python image
FROM python:3.10-slim

# Install system dependencies required to build packages
RUN apt-get update && \
    apt-get install -y gcc libpq-dev build-essential && \
    apt-get clean

# Set the working directory (adjusted based on typical Django project structure)
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables for Django
ENV PATH="/opt/venv/bin:$PATH"

# Run migrations, collect static files, and start the server
CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn AiBotsIriseUp.wsgi:application --bind 0.0.0.0:8000 --log-file -
