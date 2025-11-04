# Location: /docker/Dockerfile

# 1. Start from an official Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Set environment variables to prevent Python from buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Install system dependencies (like build-essential for some python packages)
# We will add more here later, like 'tesseract-ocr' for OCR
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python dependencies
# We copy *only* the requirements file first to leverage Docker's cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy our application's source code into the container
COPY ./src /app/src

# 7. Expose the port the app will run on
# (This is good practice, though docker-compose handles the main mapping)
EXPOSE 8000