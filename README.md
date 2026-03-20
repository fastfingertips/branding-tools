# Branding Tools

Tools for browser extension builds and assets.

## Tools

| Tool | Language | Description |
|---|---|---|
| [`tools/builder`](tools/builder/README.md) | Python | Builds Chrome, Firefox and GitHub release packages. Handles versioning and manifest conversion. |
| [`tools/icons`](tools/icons/README.md) | Node.js | Generates extension icons in standard sizes (16, 32, 48, 128) from a single source image. |

## CI Status

![CI](https://github.com/fastfingertips/branding-tools/actions/workflows/ci.yml/badge.svg)

## Reusable Actions

Both tools are available as GitHub Composite Actions for use in other repositories:

**Release Builder:**
```yaml
- uses: fastfingertips/branding-tools/.github/actions/release-builder@master
  with:
    project-path: '.'
    bump: patch
```

**Icon Generator:**
```yaml
- uses: fastfingertips/branding-tools/.github/actions/icon-generator@master
  with:
    source-image: 'assets/icon.png'
    output-dir: 'assets/icons'
```

## License

MIT
