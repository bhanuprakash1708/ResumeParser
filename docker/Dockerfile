# Location: /docker/Dockerfile

# 1. Start from an official Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Set environment variables to prevent Python from buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy our application source code
COPY ./src /app/src

# 7. Copy the tests folder into the container
COPY ./tests /app/tests
# ---------------------------

# 8. Expose the port the app will run on
EXPOSE 8000