from anyio import  to_thread
from fastapi import FastAPI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from typing import Iterator, AsyncGenerator, AsyncIterator
from pydantic import BaseModel
from app import stream_tokens, _log

app = FastAPI(title="MiniVault API (local)")


class Prompt(BaseModel):
    prompt: str


# --- 1) REST  ---------------------------------------------------------------
@app.post("/generate")
async def generate(body: Prompt):
    prompt = body.prompt
    full_text = ""
    async for chunk in stream_tokens(prompt):  # chunk is BaseMessageChunk
        full_text += chunk


    _log(prompt, full_text)

    return {"response": full_text}



# --- 2) WebSocket -----------------------------------------------------------
@app.websocket("/ws/generate")
async def ws_generate(ws: WebSocket):
    await ws.accept()
    try:
        data   = await ws.receive_json()
        prompt = data["prompt"]
        acc    = ""

        async for token in stream_tokens(prompt):
            await ws.send_text(token)
            acc += token

        await ws.close()
        _log(prompt, acc)

    except WebSocketDisconnect:
        pass
