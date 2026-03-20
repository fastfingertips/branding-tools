import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

/**
 * Universal Branding Tool - Asset Scraper & Downloader
 * 
 * Usage: 
 * node index.js --site "https://example.com" --out "./assets" --merge "merged.css"
 */

const __filename = fileURLToPath(import.meta.url);

const args = process.argv.slice(2);
const getArg = (name) => {
  const index = args.indexOf(name);
  return (index !== -1 && args[index + 1]) ? args[index + 1] : null;
};

const siteUrl = getArg('--site');
const urlsString = getArg('--urls');
const outputDir = getArg('--out') || './downloaded-assets';
const mergeFilename = getArg('--merge');

async function downloadAssets() {
  let urls = [];

  // Mode 1: Auto-scrape from a site
  if (siteUrl) {
    console.log(`Scanning ${siteUrl} for CSS and JS files...`);
    try {
      const response = await fetch(siteUrl);
      const html = await response.text();
      
      // CSS Scanner (<link rel="stylesheet">)
      const cssRegex = /<link[^>]+href=["']([^"']+\.css(?:\?[^"']*)?)["']/gi;
      // JS Scanner (<script src="...">)
      const jsRegex = /<script[^>]+src=["']([^"']+\.js(?:\?[^"']*)?)["']/gi;

      const base = new URL(siteUrl);
      
      let match;
      // Find CSS
      while ((match = cssRegex.exec(html)) !== null) {
        let assetUrl = match[1];
        if (!assetUrl.startsWith('http')) {
          assetUrl = new URL(assetUrl, base.origin).href;
        }
        urls.push(assetUrl);
      }
      
      // Find JS
      while ((match = jsRegex.exec(html)) !== null) {
        let assetUrl = match[1];
        if (!assetUrl.startsWith('http')) {
          assetUrl = new URL(assetUrl, base.origin).href;
        }
        urls.push(assetUrl);
      }

      console.log(`Found ${urls.length} files (CSS/JS) automatically.\n`);
    } catch (error) {
      console.error(`Error: Failed to scan site: ${error.message}`);
      process.exit(1);
    }
  } 
  // Mode 2: Manual URL list
  else if (urlsString) {
    urls = urlsString.split(',').map(u => u.trim());
  } else {
    console.error('Error: Provide either --site "url" or --urls "url1,url2"');
    process.exit(1);
  }

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  for (const url of urls) {
    const filename = path.basename(url).split('?')[0]; 
    const filepath = path.join(outputDir, filename);

    try {
      const response = await fetch(url);
      if (!response.ok) {
        console.log(`Skipped: ${filename} (HTTP ${response.status})`);
        continue;
      }

      const content = await response.text();
      fs.writeFileSync(filepath, content);
      console.log(`Downloaded: ${filename} (${(content.length / 1024).toFixed(1)} KB)`);
    } catch (error) {
      console.log(`Failed to download ${filename}: ${error.message}`);
    }
  }

  // Merge logic (Only for CSS)
  if (mergeFilename && mergeFilename.endsWith('.css')) {
    const mergedFile = path.join(outputDir, mergeFilename);
    const files = fs.readdirSync(outputDir).filter(f => f.endsWith('.css') && f !== mergeFilename);
    let mergedContent = '';

    for (const file of files) {
      const content = fs.readFileSync(path.join(outputDir, file), 'utf-8');
      mergedContent += `/* ===== ${file} ===== */\n${content}\n\n`;
    }

    fs.writeFileSync(mergedFile, mergedContent);
    console.log(`\nSuccessfully merged CSS into -> ${mergedFile}`);
  }
}

downloadAssets();
