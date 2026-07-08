# Use official lightweight Python image from DockerHub
FROM python:3.12-slim

# Set environment system configurations
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the functional workspace directory inside the container
WORKDIR /workspace

# Install system dependencies needed for PostgreSQL client tools compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy local dependencies schema to install packages
COPY requirements.txt /workspace/

# Install dependencies inside the container layer
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all the project modules into the image space
COPY . /workspace/

# Expose port 8000 for FastAPI API access gateway
EXPOSE 8000

# Script command execution trigger pattern
CMD ["python", "run_api.py"]