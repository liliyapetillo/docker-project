# Docker Project

My first Docker project, built while learning Docker and containerization.

## What it does

A Flask web app running behind nginx, with a PostgreSQL database — all orchestrated with Docker Compose.

## Services

- **app** - Flask API served by Gunicorn on port 8080
- **nginx** - Reverse proxy, forwards traffic to the app
- **db** - PostgreSQL database

## Setup

1. Create a `.env` file in the root:
   ```
   POSTGRES_PASSWORD=yourpassword
   ```

2. Build and start:
   ```bash
   docker build -t myapp:v1 .
   docker compose up
   ```

3. Access the app at `http://localhost`

## Endpoints

- `GET /` - Returns hello world message
- `GET /health` - Health check
