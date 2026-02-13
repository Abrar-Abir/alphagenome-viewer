"""API key validation endpoint."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class SetApiKeyRequest(BaseModel):
    api_key: str


@router.post("/api-key")
def validate_api_key(request: SetApiKeyRequest):
    """Validate an API key against the AlphaGenome API."""
    try:
        from alphagenome.models import dna_client

        dna_client.create(request.api_key.strip())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid API key: {e}")

    return {"success": True}
