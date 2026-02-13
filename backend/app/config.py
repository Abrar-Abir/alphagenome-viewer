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

# Pre-populated ontology terms (common tissues and cell lines)
ONTOLOGY_TERMS = [
    {"name": "Lung", "code": "UBERON:0002048", "type": "tissue"},
    {"name": "Brain", "code": "UBERON:0000955", "type": "tissue"},
    {"name": "Heart", "code": "UBERON:0000948", "type": "tissue"},
    {"name": "Liver", "code": "UBERON:0002107", "type": "tissue"},
    {"name": "Right liver lobe", "code": "UBERON:0001114", "type": "tissue"},
    {"name": "Kidney", "code": "UBERON:0002113", "type": "tissue"},
    {"name": "Colon - Transverse", "code": "UBERON:0001157", "type": "tissue"},
    {"name": "Stomach", "code": "UBERON:0000945", "type": "tissue"},
    {"name": "Pancreas", "code": "UBERON:0001264", "type": "tissue"},
    {"name": "Spleen", "code": "UBERON:0002106", "type": "tissue"},
    {"name": "Thyroid", "code": "UBERON:0002046", "type": "tissue"},
    {"name": "Skin", "code": "UBERON:0002097", "type": "tissue"},
    {"name": "Skeletal muscle", "code": "UBERON:0001134", "type": "tissue"},
    {"name": "Adipose tissue", "code": "UBERON:0001013", "type": "tissue"},
    {"name": "Blood", "code": "UBERON:0000178", "type": "tissue"},
    {"name": "Bone marrow", "code": "UBERON:0002371", "type": "tissue"},
    {"name": "K562 cell line", "code": "EFO:0002067", "type": "cell_line"},
    {"name": "HepG2 cell line", "code": "EFO:0001187", "type": "cell_line"},
    {"name": "GM12878 cell line", "code": "EFO:0002784", "type": "cell_line"},
]
