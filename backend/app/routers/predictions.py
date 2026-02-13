"""Prediction endpoints for genomic intervals."""

from fastapi import APIRouter, Header, HTTPException

from app.schemas.models import (
    IntervalInfo,
    IntervalPredictRequest,
    IntervalPredictResponse,
    TrackInfo,
    TrackStats,
    TranscriptInfo,
)
from app.services.alphagenome import AlphaGenomeService, get_sequence_length_name
from app.services.visualization import generate_interval_plot

router = APIRouter()


@router.post("/interval", response_model=IntervalPredictResponse)
def predict_interval(request: IntervalPredictRequest, x_api_key: str = Header(...)):
    """Predict outputs for a genomic interval."""
    # Validate interval
    if request.end <= request.start:
        raise HTTPException(
            status_code=400, detail="End position must be greater than start position"
        )

    try:
        service = AlphaGenomeService(x_api_key.strip())
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid API key: {e}")

    try:
        output_type_names = [ot.value for ot in request.output_types]
        output, interval, transcripts = service.predict_interval(
            chromosome=request.chromosome,
            start=request.start,
            end=request.end,
            output_types=output_type_names,
            ontology_terms=request.ontology_terms,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    # Generate plots for each output type
    plot_urls = []
    tracks = []

    for ot in output_type_names:
        try:
            plot_url = generate_interval_plot(output, interval, transcripts, ot)
            plot_urls.append(plot_url)

            # Extract track info from TrackData
            track_data = getattr(output, ot.lower())
            for i, row in track_data.metadata.iterrows():
                tracks.append(
                    TrackInfo(
                        output_type=ot,
                        track_name=row.get("name", ot),
                        strand=row.get("strand", "+"),
                        ontology_term=row.get("ontology_term", ""),
                        stats=TrackStats(
                            min=float(track_data.values[:, i].min()),
                            max=float(track_data.values[:, i].max()),
                            mean=float(track_data.values[:, i].mean()),
                        ),
                    )
                )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to generate plot for {ot}: {e}"
            )

    # Build transcript info
    transcript_list = []
    if hasattr(transcripts, "itertuples"):
        for t in transcripts.itertuples():
            transcript_list.append(
                TranscriptInfo(
                    gene_name=t.gene_name if hasattr(t, "gene_name") else "",
                    gene_id=t.gene_id if hasattr(t, "gene_id") else "",
                    strand=t.strand if hasattr(t, "strand") else "+",
                )
            )

    return IntervalPredictResponse(
        plot_urls=plot_urls,
        interval=IntervalInfo(
            chromosome=interval.chromosome,
            start=interval.start,
            end=interval.end,
            width=interval.width,
            sequence_length=get_sequence_length_name(interval.width),
        ),
        tracks=tracks,
        transcripts=transcript_list,
    )
