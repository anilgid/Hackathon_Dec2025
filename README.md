# AI Bot - Chat Application

A production-ready chat application with React frontend, FastAPI backend, and LLM integration.

## Features

- 🎨 **Premium Dark Mode UI** - Modern React interface with smooth animations
- ⚡ **Async Backend** - FastAPI with async request handling
- 🤖 **LLM Integration** - Supports OpenAI, Anthropic, and Google models
- 🔒 **Security** - Input sanitization, security headers, CORS protection
- 📊 **Logging** - Request/response logging with timing metrics
- 🐳 **Docker Ready** - Containerized for Google Cloud Run deployment

## Quick Start

### 1. Backend Setup

```bash
# Install dependencies
pip install -e ".[llm]"  # Install with LLM providers

# Configure LLM (copy example and edit)
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# Run backend
python -m uvicorn backend.main:app --reload
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 3. Full Stack (Production Mode)

```bash
# Build frontend
cd frontend && npm run build && cd ..

# Run full stack
python -m uvicorn backend.main:app
# Visit http://localhost:8000
```

## LLM Configuration

Edit `backend/.env`:

```env
# Choose provider: openai, anthropic, or google
LLM_PROVIDER=openai

# Add your API key
LLM_API_KEY=sk-...

# Optional: specify model
LLM_MODEL=gpt-4
```

### Supported Providers

- **OpenAI**: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`
- **Anthropic**: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`
- **Google**: `gemini-pro`, `gemini-1.5-pro`

> **Note**: The app will run in dummy mode if no LLM is configured.

## Development

### Running Tests

```bash
# Backend tests
python -m pytest tests/

# With coverage
python -m pytest --cov=backend tests/
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Cloud Run deployment instructions.

Quick deploy:
```bash
docker build -t aibot .
docker run -p 8080:8080 aibot
```

## Project Structure

```
aibot/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── api/routes.py        # API endpoints
│   ├── services/
│   │   ├── security.py      # Input sanitization
│   │   └── llm_interface.py # LLM abstraction
│   └── agents/
│       └── root_agent.py    # Agent logic
├── frontend/
│   └── src/
│       ├── components/
│       │   └── ChatInterface.tsx
│       └── api/client.ts
└── tests/
```

## License

MIT
