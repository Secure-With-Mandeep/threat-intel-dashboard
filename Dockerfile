# Use official Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (faster builds)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the project
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]

