import fs from 'fs';
import path from 'path';
import sharp from 'sharp';

/**
 * Universal Branding Tool - Extension Icon Generator
 * 
 * Usage: node index.js <source_image> <output_dir>
 */

const args = process.argv.slice(2);
const sourceImage = args[0] || 'icon.png';
const outputDir = args[1] || './icons';

const SIZES = [16, 32, 48, 128];

async function generateIcons() {
  if (!fs.existsSync(sourceImage)) {
    console.error(`Error: Source image not found: ${sourceImage}`);
    process.exit(1);
  }

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  console.log(`Generating icons from ${sourceImage}...`);

  try {
    for (const size of SIZES) {
      const outputPath = path.join(outputDir, `icon${size}.png`);
      await sharp(sourceImage)
        .resize(size, size)
        .png()
        .toFile(outputPath);
      
      console.log(`Generated ${size}x${size} -> ${outputPath}`);
    }
    console.log('\nAll icons generated successfully!');
  } catch (error) {
    console.error(`Error during generation: ${error.message}`);
    process.exit(1);
  }
}

generateIcons();
