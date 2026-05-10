# Conduit

Conduit is a lightweight Ollama-compatible bridge for cloud LLM providers.

It allows Ollama-only applications to use remote AI models from multiple providers without running local models.

---

# Features

- Ollama-compatible API (`/api/chat`, `/api/generate`, `/api/tags`, `/api/show`, `/api/version`)
- OpenAI-compatible API (`/v1/chat/completions`, `/chat/completions`)
- Multi-provider support: OpenAI, Anthropic, Google Gemini, Groq, OpenRouter
- Streaming responses
- Local lightweight daemon
- Model aliasing
- Works with Ollama-only applications

---

# Supported Providers

| Provider | Env Variable | Base URL |
|---|---|---|
| **OpenAI** | `OPENAI_API_KEY` | `https://api.openai.com/v1` |
| **Anthropic** | `ANTHROPIC_API_KEY` | `https://api.anthropic.com/v1` |
| **Google Gemini** | `GEMINI_API_KEY` | `https://generativelanguage.googleapis.com/v1beta` |
| **Groq** | `GROQ_API_KEY` | `https://api.groq.com/openai/v1` |
| **OpenRouter** | `OPENROUTER_API_KEY` | `https://openrouter.ai/api/v1` |

---

# Architecture

```text
Your App
    |
localhost:11434
    |
Conduit (Provider Factory)
    |
    +-- OpenAI ......... api.openai.com
    +-- Anthropic ...... api.anthropic.com
    +-- Gemini ......... generativelanguage.googleapis.com
    +-- Groq ........... api.groq.com
    +-- OpenRouter ..... openrouter.ai
    |
Cloud LLM
```

---

# Supported Endpoints

- `/api/chat` - Ollama chat completions (streaming)
- `/api/generate` - Ollama generate completions (streaming + non-streaming)
- `/api/tags` - List available models
- `/api/show` - Show model details
- `/api/version` - Show version
- `/v1/chat/completions` - OpenAI-compatible chat completions (streaming)
- `/chat/completions` - OpenAI-compatible chat completions (streaming)

---

# Installation

## Clone repository

```bash
git clone https://github.com/YOURNAME/conduit.git
cd conduit
```

## Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Create `.env` in the project root:

```env
# At least one of these is required
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AIza...
GROQ_API_KEY=gsk_...
OPENROUTER_API_KEY=sk-or-...
```

---

# Running

```bash
uvicorn app.main:app --host 0.0.0.0 --port 11434
```

Server will start on `http://localhost:11434`.

---

# Model Mapping

Available model aliases (configurable in `app/providers/factory.py`):

| Alias | Provider | Actual Model |
|---|---|---|
| **OpenRouter** |
| `llama3` | OpenRouter | meta-llama/llama-3.3-70b-instruct |
| `deepseek` | OpenRouter | deepseek/deepseek-chat |
| `gpt4` | OpenRouter | openai/gpt-4.1 |
| **OpenAI** |
| `gpt-4o` | OpenAI | gpt-4o |
| `gpt-4o-mini` | OpenAI | gpt-4o-mini |
| `gpt-4-turbo` | OpenAI | gpt-4-turbo |
| `gpt-3.5-turbo` | OpenAI | gpt-3.5-turbo |
| **Anthropic** |
| `claude-sonnet-4` | Anthropic | claude-sonnet-4-20250514 |
| `claude-3.5-sonnet` | Anthropic | claude-3-5-sonnet-20241022 |
| `claude-3.5-haiku` | Anthropic | claude-3-5-haiku-20241022 |
| **Gemini** |
| `gemini-2.5-pro` | Gemini | gemini-2.5-pro |
| `gemini-2.5-flash` | Gemini | gemini-2.5-flash |
| `gemini-2.0-flash` | Gemini | gemini-2.0-flash |
| **Groq** |
| `llama3-70b` | Groq | llama3-70b-8192 |
| `llama3-8b` | Groq | llama3-8b-8192 |
| `mixtral` | Groq | mixtral-8x7b-32768 |
| `gemma2` | Groq | gemma2-9b-it |

Unknown model names are routed by prefix: `gpt-*`, `o1-*`, `o3-*` → OpenAI; `claude-*` → Anthropic; `gemini-*` → Gemini; everything else → OpenRouter.

---

# Usage

```bash
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o-mini", "prompt": "hello", "stream": false}'
```

```bash
curl http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{"model": "claude-sonnet-4", "messages": [{"role": "user", "content": "hello"}], "stream": true}'
```

---

# Compatibility

Tested with:
- Ollama-compatible clients
- OpenAI-compatible clients (via `/v1/chat/completions`)

---

# Disclaimer

Conduit is not affiliated with Ollama. It only emulates parts of the Ollama API for compatibility purposes.

---

# License

MIT
