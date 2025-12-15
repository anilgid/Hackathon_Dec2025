# Deployment Guide - Cloud Run

This document describes how to deploy the AI Bot application to Google Cloud Run.

## Prerequisites

- Google Cloud SDK (`gcloud`) installed
- Docker installed locally
- A GCP project with Cloud Run API enabled
- Proper GCP authentication configured

## Local Development

### Backend Only
```bash
# Activate virtual environment
source .venv/bin/activate

# Run backend server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Only
```bash
cd frontend
npm install
npm run dev
```

### Full Stack (Production Mode)
```bash
# Build frontend
cd frontend
npm install
npm run build
cd ..

# Run backend (serves frontend)
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## Docker Build & Test

```bash
# Build the Docker image
docker build -t aibot:latest .

# Run locally
docker run -p 8080:8080 aibot:latest

# Test at http://localhost:8080
```

## Deploy to Cloud Run

### Step 1: Configure GCP Project
```bash
# Set your project ID
export PROJECT_ID=<your-gcp-project-id>
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 2: Build and Push to Container Registry
```bash
# Build for Cloud Run
docker build -t gcr.io/$PROJECT_ID/aibot:latest .

# Push to GCR
docker push gcr.io/$PROJECT_ID/aibot:latest
```

### Step 3: Deploy to Cloud Run
```bash
gcloud run deploy aibot \
  --image gcr.io/$PROJECT_ID/aibot:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1
```

### Step 4: Access Your Application
After deployment, Cloud Run will provide a URL like:
```
https://aibot-<hash>-uc.a.run.app
```

## Environment Variables (Optional)

If you need to configure environment variables:

```bash
gcloud run deploy aibot \
  --image gcr.io/$PROJECT_ID/aibot:latest \
  --set-env-vars "API_KEY=your-key-here"
```

## Monitoring & Logs

```bash
# View logs
gcloud run services logs read aibot --limit=50

# Get service details
gcloud run services describe aibot --region us-central1
```

## Updating the Deployment

```bash
# Rebuild and push
docker build -t gcr.io/$PROJECT_ID/aibot:latest .
docker push gcr.io/$PROJECT_ID/aibot:latest

# Redeploy
gcloud run deploy aibot \
  --image gcr.io/$PROJECT_ID/aibot:latest \
  --region us-central1
```

## Cost Optimization

Cloud Run charges only for the time your container is handling requests:
- Consider setting `--min-instances=0` for cost savings (default)
- Use `--concurrency=80` to handle multiple requests per instance
- Monitor usage in GCP Console

## Security Notes

- The dummy Root Agent is currently a placeholder
- Input sanitization is basic; enhance for production
- Consider adding authentication for production use
- Review CORS settings in `backend/main.py` for production
