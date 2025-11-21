FROM python:3.12-slim

WORKDIR /app

# Install paho-mqtt library
RUN pip install --no-cache-dir paho-mqtt==2.1.0

# Copy client scripts
COPY publisher.py subscriber.py ./

# Default command (will be overridden in docker-compose)
CMD ["python", "-u"]
