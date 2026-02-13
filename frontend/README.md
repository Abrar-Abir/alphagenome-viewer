# AlphaGenome Viewer - Frontend

React frontend for the AlphaGenome Viewer application.

## Setup

```bash
npm install
npm run dev
```

Open http://localhost:5173

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server (port 5173) |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI component primitives (Radix UI based)
- **React Query** - Server state management
- **React Hook Form + Zod** - Form handling and validation
- **Axios** - HTTP client

## Project Structure

```
src/
├── App.jsx              # Main application component
├── main.jsx             # Entry point
├── index.css            # Global styles + Tailwind
├── lib/
│   ├── api.js           # Backend API client
│   └── utils.js         # Utility functions (cn helper)
└── components/
    ├── ApiKeySetupDialog.jsx  # One-time API key setup modal
    ├── ThemeProvider.jsx      # Dark/light theme context
    ├── layout/
    │   ├── Header.jsx         # App header
    │   ├── InputPanel.jsx     # Left panel with forms
    │   └── ResultsPanel.jsx   # Right panel with results
    ├── inputs/
    │   ├── ModeSelector.jsx     # Interval/Variant/Score mode
    │   ├── IntervalInput.jsx    # Genomic interval form
    │   ├── VariantInput.jsx     # Variant input form
    │   ├── OutputTypeSelect.jsx # Output type multi-select
    │   └── OntologySelect.jsx   # Tissue/cell type select
    ├── results/
    │   ├── PlotViewer.jsx   # Display prediction plots
    │   ├── DataTable.jsx    # Tabular results display
    │   └── LoadingState.jsx # Loading indicator
    └── ui/                  # shadcn/ui primitives
        ├── alert.jsx
        ├── badge.jsx
        ├── button.jsx
        ├── card.jsx
        ├── checkbox.jsx
        ├── command.jsx
        ├── dialog.jsx
        ├── input.jsx
        ├── label.jsx
        ├── popover.jsx
        ├── radio-group.jsx
        ├── select.jsx
        ├── skeleton.jsx
        └── table.jsx
```

## Environment

In development, the Vite dev server proxies `/api`, `/plots`, and `/health` to `http://localhost:8000` (configured in `vite.config.js`). API calls use relative URLs by default.

Set `VITE_API_BASE_URL` to override the backend base URL (e.g., `VITE_API_BASE_URL=http://other-host:9000 npm run dev`). When empty (default), requests go to the same origin — this is how the Apptainer container serves everything on a single port.

## Adding UI Components

This project uses shadcn/ui patterns. To add new components, create them in `src/components/ui/` following the existing patterns with Radix UI primitives and Tailwind styling.
