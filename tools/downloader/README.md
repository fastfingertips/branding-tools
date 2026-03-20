# tools/downloader

Asset scraper and downloader that fetches CSS and JS files from a site and optionally merges CSS.

## Setup

```bash
cd tools/downloader
npm install
```

## Usage

```bash
# Automated scraping
node index.js --site "https://example.com" --out "./assets" --merge "merged.css"

# Manual URL list
node index.js --urls "url1.css, url2.js" --out "./assets"
```

| Argument | Description |
|---|---|
| `--site` | URL to scan for CSS and JS assets. |
| `--urls` | Comma-separated list of URLs to download manually. |
| `--out` | Output directory (default: `./downloaded-assets`). |
| `--merge` | Filename to merge all downloaded CSS into (e.g., `theme.css`). |

## GitHub Action

```yaml
- uses: fastfingertips/branding-tools/.github/actions/asset-downloader@master
  with:
    site-url: 'https://example.com'
    output-dir: 'assets/external'
    merge-css: 'external-styles.css'
```
