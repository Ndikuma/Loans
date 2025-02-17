# Use the official Python image
FROM python:3.12-slim

# Set environment variables to avoid Python .pyc file creation and to allow output to be unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for building packages (e.g., for psycopg2)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Run migrations and collect static files during the build process
# RUN python manage.py makemigrations --noinput
RUN python manage.py migrate --noinput
# RUN python manage.py collectstatic --noinput

# Set the entrypoint to Gunicorn for running the Django app
CMD ["gunicorn", "config.wsgi", "-b", "0.0.0.0:8000"]
