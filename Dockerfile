# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies that might be needed by rasterio or vision libraries
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure upload and instance directories exist
RUN mkdir -p uploads instance dataset

# Hugging Face Spaces runs as a non-root user (1000).
# We MUST grant full permissions to the /app folder so Flask can save images and create the SQLite database!
RUN chmod -R 777 /app

# Expose the port Hugging Face Spaces uses (7860)
EXPOSE 7860

# Run the application using Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--timeout", "120", "app:app"]
