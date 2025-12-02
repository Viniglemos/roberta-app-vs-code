# src/utils/auth.py

from fastapi import HTTPException, status, Header

API_KEY = "super-secret-key-123"  # hardcoded for now

async def get_api_key(x_api_key: str = Header(default=None)):
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key in 'x-api-key' header.",
        )

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid API key. Received: {x_api_key}",
        )

    return x_api_key