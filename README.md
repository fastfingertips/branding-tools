# Branding Tools

This repository contains shared utility scripts for managing and building browser extensions.

## Tools

### build_release.py

A professional-grade release builder for browser extensions that generates optimized ZIP packages for Chrome Web Store, Firefox (AMO), and GitHub Releases.

#### Features

- **Automated Version Bumping**: Syncs versions across manifest files.
- **Cross-Browser Adaptation**: Automatically converts Chrome manifests to Firefox-compatible formats (handles `service_worker` to `background.scripts` conversion).
- **Slug Generation**: Automatically generates URL-friendly filenames based on extension name.
- **Smart Exclusions**: Automatically excludes development files (git, vscode, node_modules, etc.) from production builds.

#### Usage

Run the script from the root of your extension project:

```bash
# Clone the tool into your project or link it
python path/to/branding-tools/build_release.py --bump patch
```

#### Arguments

- `--bump [major|minor|patch]`: Increment the version number before building.
- `--no-firefox`: Skip Firefox package generation.
- `--no-open`: Do not open the output folder after build (Windows only).
- `--path`: (Soon) Path to the extension project if not running from root.

## License

MIT
