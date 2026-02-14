"""Configuration and constants."""

import os

# Plots directory (override with $PLOTS_DIR for container deployments)
PLOTS_DIR = os.environ.get("PLOTS_DIR", os.path.join(os.getcwd(), "plots"))

# Sequence length options (in base pairs)
# Must match AlphaGenome model's supported lengths
SEQUENCE_LENGTHS = {
    16384: "16KB",
    131072: "128KB",
    524288: "512KB",
    1048576: "1MB",
}

# Output type descriptions
OUTPUT_TYPE_DESCRIPTIONS = {
    "ATAC": "ATAC-seq chromatin accessibility",
    "CAGE": "CAGE transcription start sites",
    "DNASE": "DNase-seq chromatin accessibility",
    "RNA_SEQ": "RNA sequencing gene expression",
    "CHIP_HISTONE": "ChIP-seq histone modifications",
    "CHIP_TF": "ChIP-seq transcription factors",
    "SPLICE_SITES": "Splice site predictions",
    "SPLICE_SITE_USAGE": "Splice site usage",
    "SPLICE_JUNCTIONS": "Splice junctions",
    "CONTACT_MAPS": "3D chromatin contacts",
    "PROCAP": "PRO-cap nascent transcription",
}
