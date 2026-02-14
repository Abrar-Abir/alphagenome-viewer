"""Pydantic schemas for request/response validation."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class OutputType(str, Enum):
    """Available AlphaGenome output types."""

    ATAC = "ATAC"
    CAGE = "CAGE"
    DNASE = "DNASE"
    RNA_SEQ = "RNA_SEQ"
    CHIP_HISTONE = "CHIP_HISTONE"
    CHIP_TF = "CHIP_TF"
    SPLICE_SITES = "SPLICE_SITES"
    SPLICE_SITE_USAGE = "SPLICE_SITE_USAGE"
    SPLICE_JUNCTIONS = "SPLICE_JUNCTIONS"
    CONTACT_MAPS = "CONTACT_MAPS"
    PROCAP = "PROCAP"


# Request schemas


class IntervalPredictRequest(BaseModel):
    """Request for interval prediction."""

    chromosome: str = Field(pattern=r"^chr([1-9]|1[0-9]|2[0-2]|X|Y)$")
    start: int = Field(gt=0)
    end: int = Field(gt=0)
    output_types: list[OutputType]
    ontology_terms: list[str] = Field(max_length=5)


class VariantRequest(BaseModel):
    """Request for variant effect prediction."""

    chromosome: str = Field(pattern=r"^chr([1-9]|1[0-9]|2[0-2]|X|Y)$")
    position: int = Field(gt=0)
    ref: str = Field(min_length=1, max_length=100)
    alt: str = Field(min_length=1, max_length=100)
    output_types: list[OutputType]
    ontology_terms: list[str] = Field(max_length=5, default=[])


class ScoreVariantRequest(BaseModel):
    """Request for variant scoring."""

    chromosome: str = Field(pattern=r"^chr([1-9]|1[0-9]|2[0-2]|X|Y)$")
    position: int = Field(gt=0)
    ref: str = Field(min_length=1, max_length=100)
    alt: str = Field(min_length=1, max_length=100)
    output_types: list[OutputType]
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=100)


# Response schemas


class OutputTypeInfo(BaseModel):
    """Output type information."""

    name: str
    description: str


class OutputTypesResponse(BaseModel):
    """Response for output types endpoint."""

    output_types: list[OutputTypeInfo]


class IntervalInfo(BaseModel):
    """Information about a genomic interval."""

    chromosome: str
    start: int
    end: int
    width: int
    sequence_length: str


class TrackStats(BaseModel):
    """Statistics for a track."""

    min: float
    max: float
    mean: float


class TrackInfo(BaseModel):
    """Information about a prediction track."""

    output_type: str
    track_name: str
    strand: str
    ontology_term: str
    stats: TrackStats


class TranscriptInfo(BaseModel):
    """Information about a transcript."""

    gene_name: str
    gene_id: str
    strand: str


class IntervalPredictResponse(BaseModel):
    """Response for interval prediction."""

    plot_urls: list[str]
    interval: IntervalInfo
    tracks: list[TrackInfo]
    transcripts: list[TranscriptInfo]


class VariantInfo(BaseModel):
    """Information about a variant."""

    chromosome: str
    position: int
    ref: str
    alt: str


class ComparisonInfo(BaseModel):
    """Comparison information for variant prediction."""

    output_type: str
    affected_genes: list[str]
    summary: str


class VariantPredictResponse(BaseModel):
    """Response for variant effect prediction."""

    plot_urls: list[str]
    variant: VariantInfo
    interval: IntervalInfo
    comparison: list[ComparisonInfo]


class VariantScore(BaseModel):
    """Score for a variant effect."""

    gene_name: str
    gene_id: str
    strand: str
    ontology_term: str
    biosample_name: str
    raw_score: float
    quantile_score: float
    output_type: str


class PaginationInfo(BaseModel):
    """Pagination information."""

    total: int
    page: int
    page_size: int


class ScoreVariantResponse(BaseModel):
    """Response for variant scoring."""

    variant: VariantInfo
    scores: list[VariantScore]
    pagination: PaginationInfo
