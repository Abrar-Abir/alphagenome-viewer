"""Visualization service for generating plots."""

import os
import uuid

import matplotlib

matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
from alphagenome.visualization import plot_components

from app.config import PLOTS_DIR


def ensure_plots_dir():
    """Ensure plots directory exists."""
    os.makedirs(PLOTS_DIR, exist_ok=True)


def generate_interval_plot(output, interval, transcripts, output_type: str) -> str:
    """Generate plot for interval predictions.

    Args:
        output: AlphaGenome prediction output
        interval: Genomic interval
        transcripts: Transcript annotations
        output_type: Output type name (e.g., "RNA_SEQ")

    Returns:
        URL path to the generated plot
    """
    ensure_plots_dir()

    track_data = getattr(output, output_type.lower())

    fig = plot_components.plot(
        components=[
            plot_components.TranscriptAnnotation(transcripts),
            plot_components.Tracks(track_data),
        ],
        interval=track_data.interval,
    )

    filename = f"{uuid.uuid4().hex}_{output_type.lower()}.png"
    filepath = os.path.join(PLOTS_DIR, filename)
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()

    return f"/plots/{filename}"


def generate_variant_plot(
    variant_output, variant, interval, transcripts, output_type: str
) -> str:
    """Generate overlay plot for variant REF/ALT comparison.

    Args:
        variant_output: AlphaGenome variant prediction output
        variant: Variant object
        interval: Genomic interval
        transcripts: Transcript annotations
        output_type: Output type name (e.g., "RNA_SEQ")

    Returns:
        URL path to the generated plot
    """
    ensure_plots_dir()

    ref_track = getattr(variant_output.reference, output_type.lower())
    alt_track = getattr(variant_output.alternate, output_type.lower())

    fig = plot_components.plot(
        [
            plot_components.TranscriptAnnotation(transcripts),
            plot_components.OverlaidTracks(
                tdata={"REF": ref_track, "ALT": alt_track},
                colors={"REF": "dimgrey", "ALT": "red"},
            ),
        ],
        interval=ref_track.interval,
        annotations=[plot_components.VariantAnnotation([variant], alpha=0.8)],
    )

    filename = f"{uuid.uuid4().hex}_variant_{output_type.lower()}.png"
    filepath = os.path.join(PLOTS_DIR, filename)
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()

    return f"/plots/{filename}"
