# AIWatchdog

AIWatchdog is an AI governance/compliance middleware designed to inspect and classify LLM-generated outputs across key safety, compliance, and ethical dimensions. It evaluates model responses using multi-agent analysis to detect hallucinations, bias, safety violations, legal risks, and ethical breaches. The system flags issues, provides explainability, and returns a structured JSON output for traceability and remediation, ensuring responsible AI usage.

Supports OpenAI, Anthropic, AWS Bedrock, Google Gemini, and Google Vertex AI.

## Features

- **5 Compliance Agents** — Data Privacy, AI Ethics, Content Compliance, Standards & Quality, Legal & Regulatory
- **Multi-Provider** — Bring your own API keys for 5 major AI providers
- **Enterprise Dashboard** — React/Next.js frontend with analytics, provider management, and settings
- **Performance Optimizations** — Intelligent batching (30-50% cost savings), smart caching (70-90% hit rate), connection pooling
- **BYOK Model** — Users configure their own provider credentials; no infrastructure costs
- **REST API** — FastAPI with auto-generated Swagger docs at `/docs`
- **API Key Auth** — Built-in authentication with key management
- **Batch Processing** — Concurrent multi-agent analysis with streaming support

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+ (for dashboard)

### Backend

```bash
# Set up virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start the API server
python main.py
```

API available at `http://localhost:8000` | Docs at `http://localhost:8000/docs`

### Dashboard

```bash
cd dashboard
npm install
npm run dev
```

Dashboard available at `http://localhost:3000`

## API Overview

### Governance Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/govern" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Content to analyze",
    "provider": "openai",
    "model": "gpt-4"
  }'
```

Returns compliance scores and violations from all 5 agents.

### Provider Configuration

```bash
curl -X POST "http://localhost:8000/api/v1/providers/openai/configure" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "sk-..."}'
```

### Available Providers

| Provider | Models | Config |
|----------|--------|--------|
| OpenAI | GPT-4o, GPT-4, GPT-3.5 Turbo | API Key |
| Anthropic | Claude 3 Opus, Sonnet, Haiku | API Key |
| AWS Bedrock | Llama 3.3, Claude on AWS | Access Key + Secret |
| Google Gemini | Gemini Pro, Pro Vision | API Key |
| Google Vertex AI | Gemini Pro, Text Bison | Service Account |

## Architecture

```
dashboard/  (Next.js 14 + TypeScript + Tailwind)
    |
    | REST API
    v
backend/    (FastAPI + Python)
    |
    |--- 5 Compliance Agents (concurrent)
    |--- Provider Adapters (OpenAI, Anthropic, etc.)
    |--- Performance Layer (caching, batching, pooling)
    |
    v
AI Providers (user-configured API keys)
```

### Compliance Agents

1. **Data Privacy & Security** — PII detection, GDPR, CCPA compliance
2. **AI Risk & Ethics** — Bias detection, fairness, ethical concerns
3. **Content & Platform Compliance** — Harmful content, misinformation
4. **Standards & Quality** — Accuracy, reliability, quality assessment
5. **Legal & Regulatory** — Cross-jurisdictional legal compliance

## Documentation

- `PROJECT_SUMMARY.md` — Technical architecture overview
- `QUICK_START.md` — 2-minute setup guide
- `COMPLETE_DASHBOARD_GUIDE.md` — Full feature documentation
- `INDEX.md` — Complete package overview

## Deployment

### Docker

```bash
docker build -t ai-governance .
docker run -p 8000:8000 -p 3000:3000 ai-governance
```

### AWS Lambda

```bash
python create_docker_package.py
# Upload the generated lambda_deployment_package.zip to AWS Lambda
```

## Tech Stack

**Backend:** Python 3.12, FastAPI, Pydantic, Uvicorn, SQLAlchemy, Redis

**Frontend:** Next.js 14, React 18, TypeScript, Tailwind CSS, Recharts, Zustand

**Infrastructure:** Docker, AWS Lambda, PostgreSQL, Redis

## License

MIT
