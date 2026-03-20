# tools/icons

Generates extension icons from a PNG image.

## Prerequisites

- Node.js 20+
- A source PNG image (recommended minimum 128x128)

## Setup

```bash
cd tools/icons
npm install
```

## Usage

```bash
node index.js <source_image> <output_dir>
```

| Argument | Default | Description |
|---|---|---|
| `source_image` | `icon.png` | Path to the source PNG. |
| `output_dir` | `./icons` | Directory to write generated icons. |

## Output

Generates the following files in `output_dir`:

- `icon16.png`
- `icon32.png`
- `icon48.png`
- `icon128.png`

## GitHub Action

```yaml
- uses: fastfingertips/branding-tools/.github/actions/icon-generator@master
  with:
    source-image: 'assets/icon.png'
    output-dir: 'assets/icons'
```
