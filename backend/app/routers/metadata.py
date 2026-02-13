"""Metadata endpoints for output types and ontology terms."""

from typing import Optional

from fastapi import APIRouter, Query

from app.config import ONTOLOGY_TERMS, OUTPUT_TYPE_DESCRIPTIONS
from app.schemas.models import (
    OntologyTerm,
    OntologyTermsResponse,
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


@router.get("/ontology-terms", response_model=OntologyTermsResponse)
def get_ontology_terms(search: Optional[str] = Query(None, description="Search term")):
    """Get ontology terms, optionally filtered by search."""
    terms = ONTOLOGY_TERMS

    if search:
        search_lower = search.lower()
        terms = [
            t
            for t in terms
            if search_lower in t["name"].lower() or search_lower in t["code"].lower()
        ]

    return OntologyTermsResponse(
        terms=[OntologyTerm(**t) for t in terms]
    )
