# Stage 1: Build frontend
FROM node:20-slim AS builder

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/app ./app

# Copy built frontend from builder stage
COPY --from=builder /app/frontend/dist ./frontend_dist

# Create writable data directories (volume mount targets)
RUN mkdir -p /app/data/plots

ENV PLOTS_DIR=/app/data/plots
ENV FRONTEND_DIST_DIR=/app/frontend_dist
ENV CORS_ORIGINS="*"
ENV AGVIEWER_PORT=8000
ENV AGVIEWER_HOST=0.0.0.0
ENV AGVIEWER_WORKERS=1

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD uvicorn app.main:app \
    --host "${AGVIEWER_HOST}" \
    --port "${AGVIEWER_PORT}" \
    --workers "${AGVIEWER_WORKERS}"
