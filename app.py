
from typing import Iterator, AsyncIterator
import json, time, pathlib, os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, BaseMessageChunk

from dotenv import load_dotenv          #  ← NEW LINE
load_dotenv()

# ----------
#  SETTINGS
# ----------
OLLAMA_URL   = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL",   "tinyllama:1.1b-chat")

# ----------
#  LLM WRAPPER
# ----------
llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.7,
    stream=True,
)

async def stream_tokens(prompt: str) -> AsyncIterator[str]:
    """Yield raw tokens from the local model."""
    messages = [
        ("human", prompt),
    ]

    async for chunk in llm.astream(messages):  # chunk is BaseMessageChunk
        yield chunk.content

# ----------
#  LOGGER
# ----------
LOG_PATH = pathlib.Path("logs/log.jsonl")
LOG_PATH.parent.mkdir(exist_ok=True)

def _log(prompt: str, response: str) -> None:
    entry = {"ts": time.time(), "prompt": prompt, "response": response}
    with LOG_PATH.open("a") as f:
        f.write(json.dumps(entry) + "\n")

