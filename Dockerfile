# Use official lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Run gunicorn server for Flask app
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
