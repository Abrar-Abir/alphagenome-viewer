<p align="center">
  <img src="https://raw.githubusercontent.com/Abrar-Abir/alphagenome-viewer/main/frontend/public/logo.png" alt="AlphaGenome Viewer" width="280">
</p>

<p align="center">
  A web interface for Google DeepMind's <a href="https://deepmind.google/blog/alphagenome-ai-for-better-understanding-the-genome/">AlphaGenome</a> genomic prediction model.
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#features">Features</a> &middot;
  <a href="#deployment">Deployment</a> &middot;
  <a href="#license">License</a>
</p>

---

## What is this?

AlphaGenome Viewer gives you a point-and-click interface to query AlphaGenome predictions — no notebook or SDK boilerplate required. Enter a genomic region or variant, pick your output types and tissues, and get back publication-ready plots and scores in seconds.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Abrar-Abir/alphagenome-viewer/main/docs/dark_mode.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Abrar-Abir/alphagenome-viewer/main/docs/light_mode.png">
    <img alt="AlphaGenome Viewer screenshot" src="https://raw.githubusercontent.com/Abrar-Abir/alphagenome-viewer/main/docs/light_mode.png" width="700">
  </picture>
</p>

## Features

**Interval Predictions** — Visualize gene expression, chromatin accessibility, histone marks, and more across any genomic region.

**Variant Effect Comparison** — Overlay REF vs ALT predictions side-by-side to see exactly how a variant changes the signal.

**Variant Scoring** — Score variants with AlphaGenome's recommended scorers and get quantile rankings across the genome.

### Supported output types

| Category | Types |
|----------|-------|
| Expression | RNA-seq, CAGE, PRO-cap |
| Accessibility | ATAC-seq, DNase-seq |
| Chromatin | ChIP-seq (histones), ChIP-seq (TFs), Contact maps |
| Splicing | Splice sites, Splice site usage, Splice junctions |

## Quick Start

### Option A: pip install (simplest)

```bash
pip install alphagenome-viewer
alphagenome-viewer
```

Open **http://localhost:8000** and enter your API key when prompted. The command accepts `--port`, `--host`, `--workers`, and `--plots-dir` flags.

### Option B: From source

#### Prerequisites

- Python 3.10+
- Node.js 18+
- [AlphaGenome API key](https://aistudio.google.com/apikey)

#### Install & Run

```bash
# Clone the repo
git clone https://github.com/Abrar-Abir/alphagenome-viewer.git
cd alphagenome-viewer

# Install dependencies
cd backend && pip install -r requirements.txt && cd ..
cd frontend && npm install && cd ..

# Start both services
./start.sh
```

You should see output like this:

```
Starting AlphaGenome Viewer...

Starting backend on http://localhost:8000...
Backend started (PID 20094, logging to backend/app.log)
Starting frontend on http://localhost:5173...
Frontend started (PID 20134, logging to frontend/app.log)

Both services running. Press Ctrl+C to stop.
  Backend:  http://localhost:8000 (logs: backend/app.log)
  Frontend: http://localhost:5173 (logs: frontend/app.log)
```

Open **http://localhost:5173** and enter your API key when prompted. That's it.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Abrar-Abir/alphagenome-viewer/main/docs/dialog_dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Abrar-Abir/alphagenome-viewer/main/docs/dialog_light.png">
    <img alt="API key setup dialog" src="https://raw.githubusercontent.com/Abrar-Abir/alphagenome-viewer/main/docs/dialog_light.png" width="400">
  </picture>
</p>

Press `Ctrl+C` to stop both services:

```
^C
Shutting down...
[2]+  Terminated              npm run dev > app.log 2>&1
Shutdown complete.
```

> You can also run the services separately — see [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md) for details.

## Deployment

### Docker

```bash
docker compose up
```

Open **http://localhost:8000**. Generated plots persist across restarts via a Docker volume. Your API key is stored in your browser's localStorage.

To build and run manually:

```bash
docker build -t alphagenome-viewer .
docker run -p 8000:8000 -v agplots:/app/data/plots alphagenome-viewer
```

### Apptainer / Singularity

For shared servers or HPC environments, build a single container — no Node.js needed at runtime:

```bash
apptainer build alphagenome-viewer.sif alphagenome-viewer.def

mkdir -p ./data/plots
apptainer run \
    --bind ./data/plots:/opt/alphagenome-viewer/data/plots \
    alphagenome-viewer.sif
```

Open **http://localhost:8000**. Change the port with `APPTAINERENV_AGVIEWER_PORT=9000`.

See `apptainer run-help alphagenome-viewer.sif` for the full list of environment variables and bind mount paths.

## Tech Stack

- **Frontend**: React, Vite, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI, Matplotlib
- **API**: [AlphaGenome SDK](https://github.com/google-deepmind/alphagenome)

## Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change.

## License

[MIT](LICENSE)

This project uses open-source dependencies under their own licenses. See [THIRD-PARTY-NOTICES](THIRD-PARTY-NOTICES) for details.
