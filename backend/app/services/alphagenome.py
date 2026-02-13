"""AlphaGenome API wrapper service."""

import pandas as pd
from alphagenome.data import gene_annotation, genome
from alphagenome.data import transcript as transcript_utils
from alphagenome.models import dna_client, variant_scorers

from app.config import SEQUENCE_LENGTHS

# GTF URL for gene annotations
GTF_URL = (
    "https://storage.googleapis.com/alphagenome/reference/gencode/"
    "hg38/gencode.v46.annotation.gtf.gz.feather"
)


def get_sequence_length(interval_width: int) -> int:
    """Auto-select smallest sequence length that fits interval."""
    for length in sorted(SEQUENCE_LENGTHS.keys()):
        if interval_width <= length:
            return length
    return max(SEQUENCE_LENGTHS.keys())


def get_sequence_length_name(length: int) -> str:
    """Get human-readable name for sequence length."""
    return SEQUENCE_LENGTHS.get(length, f"{length}bp")


class AlphaGenomeService:
    """Service for interacting with AlphaGenome API."""

    _gtf_cache: pd.DataFrame | None = None
    _transcript_extractor_cache = None

    def __init__(self, api_key: str):
        """Initialize service with API key."""
        self.client = dna_client.create(api_key)
        self._load_gtf()

    @classmethod
    def _load_gtf(cls):
        """Load gene annotations (cached at class level)."""
        if cls._gtf_cache is None:
            cls._gtf_cache = pd.read_feather(GTF_URL)
            gtf_transcripts = gene_annotation.filter_protein_coding(cls._gtf_cache)
            gtf_transcripts = gene_annotation.filter_to_mane_select_transcript(
                gtf_transcripts
            )
            cls._transcript_extractor_cache = transcript_utils.TranscriptExtractor(
                gtf_transcripts
            )

    @property
    def transcript_extractor(self):
        """Get transcript extractor (cached)."""
        return self._transcript_extractor_cache

    def predict_interval(
        self,
        chromosome: str,
        start: int,
        end: int,
        output_types: list[str],
        ontology_terms: list[str],
    ):
        """Make predictions for a genomic interval.

        Args:
            chromosome: Chromosome (e.g., "chr19")
            start: Start position
            end: End position
            output_types: List of output type names
            ontology_terms: List of ontology term codes

        Returns:
            Tuple of (output, resized_interval, transcripts)
        """
        interval = genome.Interval(chromosome, start, end)
        seq_length = get_sequence_length(interval.width)
        interval = interval.resize(seq_length)

        requested_outputs = [
            getattr(dna_client.OutputType, ot) for ot in output_types
        ]

        output = self.client.predict_interval(
            interval=interval,
            requested_outputs=requested_outputs,
            ontology_terms=ontology_terms,
        )

        transcripts = self.transcript_extractor.extract(interval)

        return output, interval, transcripts

    def predict_variant(
        self,
        chromosome: str,
        position: int,
        ref: str,
        alt: str,
        output_types: list[str],
        ontology_terms: list[str],
    ):
        """Make REF/ALT predictions for a variant.

        Args:
            chromosome: Chromosome (e.g., "chr22")
            position: Variant position
            ref: Reference allele
            alt: Alternate allele
            output_types: List of output type names
            ontology_terms: List of ontology term codes

        Returns:
            Tuple of (variant_output, variant, interval, transcripts)
        """
        variant = genome.Variant(
            chromosome=chromosome,
            position=position,
            reference_bases=ref,
            alternate_bases=alt,
        )

        # Use smallest sequence length for single-position variants
        interval = variant.reference_interval.resize(get_sequence_length(1))

        requested_outputs = [
            getattr(dna_client.OutputType, ot) for ot in output_types
        ]

        variant_output = self.client.predict_variant(
            interval=interval,
            variant=variant,
            requested_outputs=requested_outputs,
            ontology_terms=ontology_terms,
        )

        transcripts = self.transcript_extractor.extract(interval)

        return variant_output, variant, interval, transcripts

    def score_variant(
        self,
        chromosome: str,
        position: int,
        ref: str,
        alt: str,
        output_types: list[str],
    ) -> pd.DataFrame:
        """Score variant effects using recommended scorers.

        Args:
            chromosome: Chromosome (e.g., "chr22")
            position: Variant position
            ref: Reference allele
            alt: Alternate allele
            output_types: List of output type names

        Returns:
            DataFrame with variant scores
        """
        variant = genome.Variant(
            chromosome=chromosome,
            position=position,
            reference_bases=ref,
            alternate_bases=alt,
        )

        interval = variant.reference_interval.resize(dna_client.SEQUENCE_LENGTH_1MB)

        all_scores = []
        for ot in output_types:
            scorer = variant_scorers.RECOMMENDED_VARIANT_SCORERS[ot]
            scores = self.client.score_variant(
                interval=interval,
                variant=variant,
                variant_scorers=[scorer],
            )
            tidy = variant_scorers.tidy_scores(scores, match_gene_strand=True)
            tidy["output_type"] = ot
            all_scores.append(tidy)

        if all_scores:
            return pd.concat(all_scores, ignore_index=True)
        return pd.DataFrame()
