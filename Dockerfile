# Use a build-time argument for the Python version
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a virtual environment and set it in the PATH
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

# Install system dependencies in a single layer to minimize image size
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libpq-dev \
    libjpeg-dev \
    libcairo2 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set up the application directory
WORKDIR /code

# Copy requirements and install them
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the application source code
COPY ./src /code

# Run static file collection
RUN python manage.py collectstatic --noinput

# Set the Django project name
ARG PROJ_NAME="cfehome"

# Create and make the runner script executable
RUN printf "#!/bin/bash\n" > ./paracord_runner.sh && \
    printf "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./paracord_runner.sh && \
    printf "python manage.py migrate --no-input\n" >> ./paracord_runner.sh && \
    printf "gunicorn ${PROJ_NAME}.wsgi:application --bind \"[::]:\$RUN_PORT\"\n" >> ./paracord_runner.sh && \
    chmod +x paracord_runner.sh

# Expose the port where the application will run
EXPOSE 8000

# The command to run the application
CMD ./paracord_runner.sh