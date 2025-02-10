# Use the official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Ensure the start script is executable
RUN chmod +x /app/scripts/start.sh

# Set the entrypoint to the script
ENTRYPOINT ["/bin/sh", "/app/scripts/start.sh"]
