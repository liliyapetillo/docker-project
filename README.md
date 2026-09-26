# Docker Project

A Flask web app, containerized and served by Gunicorn, meant to run directly on ECS/Fargate — no reverse proxy or database in front of it.

## Setup

1. Build the image:
   ```bash
   docker build -t myapp:v1 .
   ```

2. Run it:
   ```bash
   docker run -p 8080:8080 myapp:v1
   ```

3. Access the app at `http://localhost:8080`

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Endpoints

- `GET /` - Returns hello world message
- `GET /health` - Health check
