# Slim base image
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Send print() output to CloudWatch immediately instead of buffering it
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code after dependencies so code changes don't invalidate the pip install layer
COPY app.py .
COPY static/ static/
COPY templates/ templates/
COPY prompts/ prompts/

# Document the port the app listens on (publishing is done by ECS / docker run -p)
EXPOSE 8080

# Serve with gunicorn instead of the Flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
