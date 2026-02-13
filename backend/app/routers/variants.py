"""Variant effect prediction and scoring endpoints."""

from fastapi import APIRouter, Header, HTTPException

from app.schemas.models import (
    ComparisonInfo,
    IntervalInfo,
    PaginationInfo,
    ScoreVariantRequest,
    ScoreVariantResponse,
    VariantInfo,
    VariantPredictResponse,
    VariantRequest,
    VariantScore,
)
from app.services.alphagenome import AlphaGenomeService, get_sequence_length_name
from app.services.visualization import generate_variant_plot

router = APIRouter()


@router.post("/predict/variant", response_model=VariantPredictResponse)
def predict_variant(request: VariantRequest, x_api_key: str = Header(...)):
    """Predict variant effects (REF vs ALT comparison)."""
    try:
        service = AlphaGenomeService(x_api_key.strip())
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid API key: {e}")

    try:
        output_type_names = [ot.value for ot in request.output_types]
        variant_output, variant, interval, transcripts = service.predict_variant(
            chromosome=request.chromosome,
            position=request.position,
            ref=request.ref,
            alt=request.alt,
            output_types=output_type_names,
            ontology_terms=request.ontology_terms,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Variant prediction failed: {e}")

    # Generate plots for each output type
    plot_urls = []
    comparisons = []

    for ot in output_type_names:
        try:
            plot_url = generate_variant_plot(
                variant_output, variant, interval, transcripts, ot
            )
            plot_urls.append(plot_url)

            # Extract affected genes from transcripts
            affected_genes = []
            if hasattr(transcripts, "itertuples"):
                for t in transcripts.itertuples():
                    if hasattr(t, "gene_name") and t.gene_name:
                        affected_genes.append(t.gene_name)
            affected_genes = list(set(affected_genes))[:5]  # Limit to 5

            comparisons.append(
                ComparisonInfo(
                    output_type=ot,
                    affected_genes=affected_genes,
                    summary=f"Comparison of REF ({request.ref}) vs ALT ({request.alt})",
                )
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to generate variant plot for {ot}: {e}"
            )

    return VariantPredictResponse(
        plot_urls=plot_urls,
        variant=VariantInfo(
            chromosome=request.chromosome,
            position=request.position,
            ref=request.ref,
            alt=request.alt,
        ),
        interval=IntervalInfo(
            chromosome=interval.chromosome,
            start=interval.start,
            end=interval.end,
            width=interval.width,
            sequence_length=get_sequence_length_name(interval.width),
        ),
        comparison=comparisons,
    )


@router.post("/score/variant", response_model=ScoreVariantResponse)
def score_variant(request: ScoreVariantRequest, x_api_key: str = Header(...)):
    """Score variant effects using recommended scorers."""
    try:
        service = AlphaGenomeService(x_api_key.strip())
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid API key: {e}")

    try:
        output_type_names = [ot.value for ot in request.output_types]
        scores_df = service.score_variant(
            chromosome=request.chromosome,
            position=request.position,
            ref=request.ref,
            alt=request.alt,
            output_types=output_type_names,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Variant scoring failed: {e}")

    # Convert DataFrame to response
    total = len(scores_df)
    start_idx = (request.page - 1) * request.page_size
    end_idx = start_idx + request.page_size

    scores = []
    if not scores_df.empty:
        page_df = scores_df.iloc[start_idx:end_idx]
        for _, row in page_df.iterrows():
            scores.append(
                VariantScore(
                    gene_name=str(row.get("gene_name", "")),
                    gene_id=str(row.get("gene_id", "")),
                    strand=str(row.get("strand", "+")),
                    ontology_term=str(row.get("ontology_term", "")),
                    biosample_name=str(row.get("biosample_name", "")),
                    raw_score=float(row.get("raw_score", 0.0)),
                    quantile_score=float(row.get("quantile_score", 0.0)),
                    output_type=str(row.get("output_type", "")),
                )
            )

    return ScoreVariantResponse(
        variant=VariantInfo(
            chromosome=request.chromosome,
            position=request.position,
            ref=request.ref,
            alt=request.alt,
        ),
        scores=scores,
        pagination=PaginationInfo(
            total=total,
            page=request.page,
            page_size=request.page_size,
        ),
    )
