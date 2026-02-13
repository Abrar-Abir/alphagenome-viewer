# AlphaGenome Viewer - Backend

FastAPI backend for AlphaGenome genomic predictions.

## Setup

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PLOTS_DIR` | `plots/` | Directory for generated plot PNGs |
| `CORS_ORIGINS` | `http://localhost:5173` | Comma-separated allowed origins |
| `FRONTEND_DIST_DIR` | _(unset)_ | Built frontend directory — only set in container deployments |
| `AGVIEWER_PORT` | `8000` | Port to listen on (used by Docker/Apptainer) |
| `AGVIEWER_HOST` | `0.0.0.0` | Host to bind to (used by Docker/Apptainer) |
| `AGVIEWER_WORKERS` | `1` | Number of uvicorn workers (used by Docker/Apptainer) |

## API Endpoints

### Configuration

| Endpoint | Description |
|----------|-------------|
| `POST /api/config/api-key` | Validate an API key |

### Metadata

| Endpoint | Description |
|----------|-------------|
| `GET /api/metadata/output-types` | List available prediction output types (RNA_SEQ, DNASE, etc.) |
| `GET /api/metadata/ontology-terms?search=` | Search tissue/cell type ontology terms |

### Predictions

| Endpoint | Description |
|----------|-------------|
| `POST /api/predict/interval` | Predict outputs for a genomic interval |
| `POST /api/predict/variant` | Compare REF vs ALT predictions for a variant |
| `POST /api/score/variant` | Score variant effects using recommended scorers |

### Health

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |

## Request Examples

### Validate API Key

```bash
curl -X POST http://localhost:8000/api/config/api-key \
  -H "Content-Type: application/json" \
  -d '{"api_key": "your-key"}'
```

### Interval Prediction

```bash
curl -X POST http://localhost:8000/api/predict/interval \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{
    "chromosome": "chr19",
    "start": 40991281,
    "end": 41018398,
    "output_types": ["RNA_SEQ"],
    "ontology_terms": ["UBERON:0002048"]
  }'
```

### Variant Prediction

```bash
curl -X POST http://localhost:8000/api/predict/variant \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{
    "chromosome": "chr22",
    "position": 36201698,
    "ref": "A",
    "alt": "C",
    "output_types": ["RNA_SEQ"],
    "ontology_terms": ["UBERON:0001157"]
  }'
```

### Variant Scoring

```bash
curl -X POST http://localhost:8000/api/score/variant \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{
    "chromosome": "chr22",
    "position": 36201698,
    "ref": "A",
    "alt": "C",
    "output_types": ["RNA_SEQ"],
    "page": 1,
    "page_size": 50
  }'
```

## Project Structure

```
app/
├── main.py              # FastAPI app entry point
├── cli.py               # CLI entry point (alphagenome-viewer command)
├── config.py            # Constants and configuration
├── routers/
│   ├── config.py        # API key validation endpoint
│   ├── metadata.py      # Metadata endpoints
│   ├── predictions.py   # Interval prediction endpoint
│   └── variants.py      # Variant prediction/scoring endpoints
├── services/
│   ├── alphagenome.py   # AlphaGenome SDK wrapper
│   └── visualization.py # Plot generation
└── schemas/
    └── models.py        # Pydantic models
```

## Output Types

- `ATAC` - ATAC-seq chromatin accessibility
- `CAGE` - CAGE transcription start sites
- `DNASE` - DNase-seq chromatin accessibility
- `RNA_SEQ` - RNA sequencing gene expression
- `CHIP_HISTONE` - ChIP-seq histone modifications
- `CHIP_TF` - ChIP-seq transcription factors
- `SPLICE_SITES` - Splice site predictions
- `SPLICE_SITE_USAGE` - Splice site usage
- `SPLICE_JUNCTIONS` - Splice junctions
- `CONTACT_MAPS` - 3D chromatin contacts
- `PROCAP` - PRO-cap nascent transcription
