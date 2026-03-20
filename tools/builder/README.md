# tools/builder

Python package for building and packaging browser extension releases.

## Prerequisites

- Python 3.11+

## Usage

Run from the root of this repository, targeting your extension project:

```bash
python -m tools.builder --path /path/to/extension --bump patch
```

## Arguments

| Argument | Description |
|---|---|
| `--path` | Path to the extension project root (must contain `manifest.json`). |
| `--bump [major\|minor\|patch]` | Increment version before building. |
| `--id` | Firefox Gecko extension ID (e.g. `app@example.com`). |
| `--no-firefox` | Skip Firefox package generation. |
| `--no-open` | Do not open output folder after build (Windows). |

## Output

Packages are written to `releases/` inside the target extension project:

| Package | Contents |
|---|---|
| `*-chrome.zip` | Chrome Web Store submission. |
| `*-firefox.zip` | Firefox (AMO) submission with converted manifest. |
| `*.zip` | GitHub Release (includes docs: README, LICENSE, etc.). |

## GitHub Action

This tool is also available as a reusable GitHub Action:

```yaml
- uses: fastfingertips/branding-tools/.github/actions/release-builder@master
  with:
    project-path: '.'
    bump: patch
```
