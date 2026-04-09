FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for OpenCV, PostgreSQL, etc.
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
# Pre-download SpaCy model for text simplification
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 8000
