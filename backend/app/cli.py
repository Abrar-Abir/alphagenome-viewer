"""CLI entry point for alphagenome-viewer."""

import argparse
import os
from pathlib import Path


def main():
    """Launch the AlphaGenome Viewer server."""
    parser = argparse.ArgumentParser(
        prog="alphagenome-viewer",
        description="AlphaGenome Viewer - Web interface for genomic predictions",
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to listen on (default: 8000)"
    )
    parser.add_argument(
        "--workers", type=int, default=1, help="Number of uvicorn workers (default: 1)"
    )
    parser.add_argument(
        "--plots-dir",
        default=None,
        help="Directory for generated plots (default: ./plots)",
    )
    args = parser.parse_args()

    # Set PLOTS_DIR: CLI arg > existing env var > default (cwd/plots)
    if args.plots_dir:
        os.environ["PLOTS_DIR"] = os.path.abspath(args.plots_dir)
    elif "PLOTS_DIR" not in os.environ:
        os.environ["PLOTS_DIR"] = os.path.join(os.getcwd(), "plots")

    # Point to bundled frontend if present and not already overridden
    if "FRONTEND_DIST_DIR" not in os.environ:
        bundled_frontend = Path(__file__).parent / "frontend_dist"
        if bundled_frontend.is_dir():
            os.environ["FRONTEND_DIST_DIR"] = str(bundled_frontend)

    import uvicorn

    print(f"Starting AlphaGenome Viewer on http://{args.host}:{args.port}")
    print(f"Plots directory: {os.environ.get('PLOTS_DIR')}")
    if os.environ.get("FRONTEND_DIST_DIR"):
        print(f"Serving frontend from: {os.environ['FRONTEND_DIST_DIR']}")
    else:
        print("No bundled frontend found - API-only mode")
    print()

    uvicorn.run("app.main:app", host=args.host, port=args.port, workers=args.workers)


if __name__ == "__main__":
    main()
