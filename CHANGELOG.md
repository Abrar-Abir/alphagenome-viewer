# Changelog

## [1.0.1] - 2026-02-14

### Fixed
- Fix startup race condition: retry network errors during server startup
- Scope jsconfig.json to src/ to fix VSCode warnings

### Changed
- Hardcode ontology terms in frontend, remove redundant backend endpoint
- Use project icon as browser tab favicon
- Add third-party license notices for dependencies

## [1.0.0] - 2025-02-13

### Added

- Web interface for AlphaGenome genomic predictions
- Three prediction modes: interval predictions, variant effect comparison, and variant scoring
- Publication-ready matplotlib track plots with gene annotations
- Output type and tissue/cell type selection with ontology search
- API key validation and browser-side storage
- Dark mode support
- Docker and Apptainer/Singularity deployment options
- pip-installable package with `alphagenome-viewer` CLI command
