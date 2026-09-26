# Slim base image
FROM python:3.12-slim

# Set working directory in the container 
WORKDIR /app

# Install dependencies 
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code after dependencies so code changes don't invalidate the pip install layer
COPY app.py .
COPY static/ static/

# Make port available for everybody outside of the container
EXPOSE 8080

# Serve with gunicorn instead of the Flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
