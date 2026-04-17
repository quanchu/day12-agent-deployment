from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from .config import settings

# ─────────────────────────────────────────────────────────
# API Key Authentication Module
# ─────────────────────────────────────────────────────────

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Dependency to verify the incoming API key.
    Checks against the AGENT_API_KEY environment variable.
    """
    if not api_key or api_key != settings.agent_api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key. Include header: X-API-Key: <key>",
        )
    return api_key
