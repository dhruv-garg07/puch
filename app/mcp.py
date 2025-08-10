from typing import Dict, Any
from fastapi import HTTPException

async def handle_mcp(*, body: Dict[str, Any], bearer_tokens: Dict[str, str]) -> Dict[str, Any]:
    tool = body.get("tool")
    args = body.get("args", {})

    # Required by Puch: must return { "phone": "<countrycode><number>" } for a valid token
    if tool == "validate":
        token = args.get("token", "")
        phone = bearer_tokens.get(token)
        if not phone:
            raise HTTPException(status_code=401, detail="Invalid bearer token")
        return {"phone": phone}

    # For the deadline: just respond with a friendly stub for any other tool.
    name = tool or "unknown"
    return {"message": f"🧪 Stub server is live. Tool '{name}' is not implemented yet."}
