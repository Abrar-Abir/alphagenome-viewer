#!/bin/bash

# AlphaGenome Viewer - Start Script
# Starts backend (background) and frontend (background)
# Ctrl+C kills both process trees, then exits

set -e
set -m  # Job control: background processes get their own process groups

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
    echo ""
    echo "Shutting down..."

    # Send SIGTERM to entire process groups (kills children too)
    for PID in "$BACKEND_PID" "$FRONTEND_PID"; do
        if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
            kill -- -"$PID" 2>/dev/null || kill "$PID" 2>/dev/null || true
        fi
    done

    # Brief wait, then SIGKILL any survivors
    sleep 1
    for PID in "$BACKEND_PID" "$FRONTEND_PID"; do
        if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
            kill -9 -- -"$PID" 2>/dev/null || kill -9 "$PID" 2>/dev/null || true
        fi
    done

    echo "Shutdown complete."
    exit 0
}

trap cleanup SIGINT SIGTERM

# Kill any stale processes from a previous run
if command -v lsof >/dev/null 2>&1 && lsof -ti:8000 >/dev/null 2>&1; then
    echo "Warning: killing stale process on port 8000..."
    kill $(lsof -ti:8000) 2>/dev/null || true
    sleep 1
fi

echo "Starting AlphaGenome Viewer..."
echo ""

# Start backend in background
echo "Starting backend on http://localhost:8000..."
cd "$SCRIPT_DIR/backend"
uvicorn app.main:app --reload --port 8000 > app.log 2>&1 &
BACKEND_PID=$!
echo "Backend started (PID $BACKEND_PID, logging to backend/app.log)"

# Wait a moment for backend to initialize
sleep 2

# Check if backend started successfully
if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
    echo "ERROR: Backend failed to start. Check backend/app.log for details."
    exit 1
fi

# Start frontend in background
echo "Starting frontend on http://localhost:5173..."
cd "$SCRIPT_DIR/frontend"
npm run dev > app.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend started (PID $FRONTEND_PID, logging to frontend/app.log)"

echo ""
echo "Both services running. Press Ctrl+C to stop."
echo "  Backend:  http://localhost:8000 (logs: backend/app.log)"
echo "  Frontend: http://localhost:5173 (logs: frontend/app.log)"
echo ""

# Wait for either process to exit
while kill -0 "$BACKEND_PID" 2>/dev/null && kill -0 "$FRONTEND_PID" 2>/dev/null; do
    wait -n 2>/dev/null || true
done

# If we get here, one process died unexpectedly
if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
    echo "ERROR: Backend exited unexpectedly. Check backend/app.log"
fi
if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
    echo "ERROR: Frontend exited unexpectedly. Check frontend/app.log"
fi
cleanup
