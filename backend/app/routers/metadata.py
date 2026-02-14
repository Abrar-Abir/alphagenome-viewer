"""Metadata endpoints for output types."""

from fastapi import APIRouter

from app.config import OUTPUT_TYPE_DESCRIPTIONS
from app.schemas.models import (
    OutputType,
    OutputTypeInfo,
    OutputTypesResponse,
)

router = APIRouter()


@router.get("/output-types", response_model=OutputTypesResponse)
def get_output_types():
    """Get available AlphaGenome output types."""
    output_types = [
        OutputTypeInfo(
            name=ot.value,
            description=OUTPUT_TYPE_DESCRIPTIONS.get(ot.value, ot.value),
        )
        for ot in OutputType
    ]
    return OutputTypesResponse(output_types=output_types)
