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

## Future Considerations: CRXJS Integration

While this custom toolset is excellent for lightweight, vanilla JS extensions, larger projects might benefit from [CRXJS (Vite-based)](https://github.com/crxjs/chrome-extension-tools).

### When to stay with Branding Tools:
- **Lightweight**: Simple architecture (Vanilla JS/CSS) with zero build dependencies.
- **Portability**: No Node.js/npm required; perfect for Python-friendly environments.
- **Deterministic**: Complete control over exactly what gets zipped into the final package.
- **Native Experience**: Ideal for developers who prefer the "Browser Native" way without bundler abstractions.

### When to consider CRXJS:
- **HMR (Hot Module Replacement)**: If you want to see UI/Content Script changes instantly without page refreshes.
- **Modern Stack**: If you move to React, Svelte, Tailwind CSS, or TypeScript.
- **Automation**: When you have many dynamic assets that need automatic `web_accessible_resources` mapping.

## License

MIT
