import os
from typing import Dict
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from dotenv import load_dotenv

from .mcp import handle_mcp

load_dotenv()

# Env vars
TOKENS_RAW = (os.getenv("BEARER_TOKENS") or "devtoken:919876543210").strip()
BEARER_TOKENS: Dict[str, str] = dict(item.split(":") for item in TOKENS_RAW.split(",")) if TOKENS_RAW else {}

app = FastAPI(title="Empty MCP Server", version="0.1.0")

@app.get("/healthz", response_class=PlainTextResponse)
async def healthz():
    return "ok"

@app.get("/diag")
async def diag():
    return JSONResponse({
        "env": {
            "BEARER_TOKENS_present": bool(BEARER_TOKENS),
            "tokens_count": len(BEARER_TOKENS),
        },
        "status": "running"
    })

@app.post("/mcp")
async def mcp(request: Request):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(400, "Invalid JSON")
    # No DB; just pass to the stub handler
    return await handle_mcp(body=body, bearer_tokens=BEARER_TOKENS)
