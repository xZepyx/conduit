# Conduit

Conduit is a lightweight Ollama-compatible bridge for cloud LLM providers.

It allows Ollama-only applications to use remote AI models from providers like OpenRouter without running local models.

---

# Features

- Ollama-compatible API
- OpenRouter support
- Streaming responses
- Local lightweight daemon
- Simple setup
- Model aliasing
- Works with Ollama-only applications

---

# Why?

Many applications support only Ollama as an AI backend.

However:

- local models are large
- GPUs are expensive
- laptops may not handle inference well

Conduit solves this by emulating the Ollama API locally while routing requests to cloud providers.

---

# Architecture

```text
Your App
    ↓
localhost:11434
    ↓
Conduit
    ↓
OpenRouter
    ↓
Cloud LLM
```

---

# Supported Endpoints

Currently implemented:

- `/api/chat`
- `/api/generate`
- `/api/tags`
- `/api/version`

---

# Installation

## Clone repository

```bash
git clone https://github.com/YOURNAME/conduit.git

cd conduit
```

---

## Create virtual environment

### Linux

```bash
python -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Create `.env`

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

# Running

```bash
uvicorn app.main:app --host 0.0.0.0 --port 11434
```

Server will start on:

```text
http://localhost:11434
```

---

# Using with Ollama Apps

Point your application to:

```text
http://localhost:11434
```

Use any configured model alias:

```text
llama3
deepseek
gpt4
```

---

# Model Mapping

Current aliases:

| Alias | Provider Model |
|---|---|
| llama3 | meta-llama/llama-3.3-70b-instruct |
| deepseek | deepseek/deepseek-chat |
| gpt4 | openai/gpt-4.1 |

Mappings are configured in:

```text
app/providers/openrouter.py
```

---

# Example Request

```bash
curl http://localhost:11434/api/generate \
-H "Content-Type: application/json" \
-d '{
  "model":"llama3",
  "prompt":"hello",
  "stream":false
}'
```

---

# Streaming

Conduit supports Ollama-style streaming responses.

Applications supporting streaming should work automatically.

---

# Compatibility

Tested with:

- custom Ollama clients
- CLI tools
- Ollama-compatible applications

More compatibility testing planned.

---

# Disclaimer

Conduit is not affiliated with Ollama.

It only emulates parts of the Ollama API for compatibility purposes.

---

# License

MIT