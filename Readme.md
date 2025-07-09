# 🧠 MiniVault API — ModelVault Take-Home

A lightweight, local REST API that simulates the core feature of ModelVault’s product: accepting a prompt and returning a generated response via a local LLM. This solution uses **FastAPI** for the API layer and **Ollama** to run lightweight models like `tinyllama:1.1b-chat` — all 100% offline.

---

## ✨ Features

- ✅ `POST /generate` — send a prompt and receive a model-generated response  
- ✅ Logs all interactions to `logs/log.jsonl`  
- ✅ Uses **local LLM only** (no OpenAI or Anthropic)  
- ✅ Dockerized setup with **modular control**  
- ✅ Environment-based model configuration via `.env`  
- ⚡️ Optional WebSocket stream endpoint (`/ws/generate`)  
- 💻 Includes CLI for quick local testing  

---

## 🧱 Directory Structure

```
minivault-api/
├── app/                     # FastAPI app code
│   ├── main.py              # Entry point (FastAPI routes)
│   ├── core.py              # LLM + logger setup
│   └── cli.py               # CLI tool for testing prompts
├── logs/log.jsonl          # Prompt/response logs
├── .env                    # Environment config (model, base URL)
├── requirements.txt        # Python dependencies
├── Dockerfile              # API container
├── docker-compose.yml      # Ollama container
├── docker-compose-app.yml  # API container (used after model is pulled)
|── README.md
└── postman_collection.json # Postman collection 

```

---

## 🚀 Setup & Usage

### Step 1: Start Ollama (model server)

We start the Ollama container **alone** so we can pull the model first.

```bash
docker compose up -d --build
```

This starts Ollama on `localhost:11434`.

---

### Step 2: Pull a lightweight local model

We use [`tinyllama:1.1b-chat`](https://huggingface.co/codellama) for speed and low memory usage (CPU-friendly).

```bash
docker exec -it ollama ollama pull tinyllama:1.1b-chat
```

✅ This downloads the model into the persistent `ollama_data` volume.

> 🧠 **Why this manual step?**  
> Pulling a model inside the API container startup causes delays and timeouts because Ollama isn’t "healthy" until the pull finishes. That’s why we **separate** the model pull step from API startup — for speed and clarity.

---

### Step 3A: Run API locally (for development)

After pulling the model, you can start FastAPI using your host Python:

```bash
# Activate your virtualenv
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the app
uvicorn app.main:app --reload
```

---

### Step 3B: Or run the API via Docker Compose

We use a **second compose file** just for the API:

```bash
docker compose -f docker-compose-app.yml up --build
```

> 💡 **Why two compose files?**
>
> - `docker-compose.yml` starts **only Ollama**, so you can pull the model first.
> - `docker-compose-app.yml` starts the **FastAPI app**, after the model is ready.
>
> This avoids model download timeouts during API boot and gives you flexibility.

---

## 🔍 Example Usage

### ✅ REST API

```http
POST /generate
Content-Type: application/json

{ "prompt": "Explain gravity in one sentence." }
```

Returns:

```json
{ "response": "Gravity is a force of attraction..." }
```

---

### 🧪 CLI Testing

```bash
python app/cli.py "Explain photosynthesis"
```

---

### 🔌 WebSocket Streaming (Optional)

```ws
ws://localhost:8000/ws/generate
```

Send JSON:

```json
{ "prompt": "Tell me a joke." }
```

---

## 📦 Environment Variables

Configure these in your `.env` file:

```env
OLLAMA_MODEL=tinyllama:1.1b-chat
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 💡 Tradeoffs & Improvement Ideas

| Area                      | Current                                      | Potential Upgrade                                                                       |
|---------------------------|----------------------------------------------|-----------------------------------------------------------------------------------------|
| **Model Setup**           | Manual pull of `tinyllama` use advance model | Automate with job queue/bootstrap health script  and use advance model likeDeepSeek-R1  |
| **Prompt Logging**        | Logs to `.jsonl` file                        | Add SQLite or Redis for searchable history                                              |
| **Stateless API**         | No conversation memory                       | Add in-memory or persistent store (e.g., LangChain Memory or sqlite or postgres)        |
| **Authentication**        | None                                         | Add API key/token-based auth                                                            |
| **Testing**               | Manual via Postman or CLI                    | Add Pytest + sample prompt tests                                                        |
| **UI / Playground**       | None                                         | Add Swagger UI or simple chat HTML front                                                |

---

## ✅ Submission Checklist

- [x] Local REST API  
- [x] Logs all interactions  
- [x] Uses a local LLM (`tinyllama`)  
- [x] CLI & WebSocket support  
- [x] Clean modular code with `.env` and Docker  
- [x] README with detailed setup & tradeoffs  

---

