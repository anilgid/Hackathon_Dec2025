# Build Stage for Frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Runtime Stage
FROM python:3.12-slim
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install python dependencies
# Using pip for simplicity in Docker, could interpret uv.lock if needed but pip is fine
COPY pyproject.toml .
# We can export requirements from uv or just install based on toml if pip supports it (modern pip does)
# Or since we don't have a requirements.txt, we can just install '.'
COPY src ./src
COPY backend ./backend
COPY README.md .

# Install dependencies including the project itself
RUN pip install --no-cache-dir . fastapi uvicorn httpx

# Copy built frontend assets
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Environment variables
ENV PORT=8080
ENV HOST=0.0.0.0

# Run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
