# Branding Tools

Shared utility scripts and packages for managing browser extension builds.

## Directory Structure

- `tools/builder`: Python package for building extension releases.
- `tools/icons`: Node.js package for generating extension icons.

## Release Builder (Python)

A release builder for browser extensions that generates optimized ZIP packages for Chrome Web Store, Firefox (AMO), and GitHub Releases.

### Features

- Automated version bumping across manifest files.
- Manifest conversion for Firefox compatibility (handles service_worker to background.scripts).
- Automatic slug generation from extension name.
- Configurable exclusion patterns (git, node_modules, etc.).

### Usage

Run from the root of your extension project:

```bash
python -m tools.builder --path . --bump patch
```

### Arguments

- `--bump [major|minor|patch]`: Increment the version number before building.
- `--no-firefox`: Skip Firefox package generation.
- `--no-open`: Do not open the output folder after build (Windows only).
- `--path`: Path to the extension project.

## Icon Generator (Node.js)

A Sharp-based tool for generating extension icons in standard sizes (16, 32, 48, 128).

### Usage

```bash
cd tools/icons
npm install
node index.js <source_image> <output_dir>
```

## License

MIT
