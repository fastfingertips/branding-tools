# Contributing

Contributions are welcome.

## Getting Started

1. Fork the repository.
2. Create a new branch: `git checkout -b your-branch-name`.
3. Make your changes.
4. Run linters before committing (see below).
5. Open a pull request against `master`.

## Code Style

**Python (tools/builder):**
```bash
pip install ruff
ruff check tools/builder
ruff format tools/builder
```

**Node.js (tools/icons):**
```bash
cd tools/icons
npm install
npm run lint
```

## Adding a New Tool

- Create a new directory under `tools/`.
- Include a `README.md` inside the tool directory explaining usage.
- Update the top-level `README.md` with a short description.

## Reporting Issues

Open an issue with a clear title and reproduction steps.
