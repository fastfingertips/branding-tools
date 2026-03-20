"""Release builder implementation for browser extensions."""
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from .manifest import Manifest

MANIFEST_FILE = 'manifest.json'

class ReleaseBuilder:
    """Handles the creation of release packages for Chrome extensions."""
    
    CHROME_FILES = [MANIFEST_FILE, 'src', 'assets']
    DOCS_FILES = ['README.md', 'PRIVACY.md', 'LICENSE', 'CHANGELOG.md']
    EXCLUDE_PATTERNS = [
        '__pycache__', '.git', '.agent', '.workflows',
        '.gitignore', '.gitattributes', 'node_modules',
        'releases', 'docs', 'scripts', '.vscode', '.idea',
        '*.zip', '*.pyc', '.DS_Store', 'Thumbs.db'
    ]
    
    def __init__(self, project_root: Optional[str] = None):
        """Initialize builder with project root directory."""
        if project_root:
            self.project_root = Path(project_root).resolve()
        elif (Path.cwd() / MANIFEST_FILE).exists():
            self.project_root = Path.cwd()
        else:
            print(f"Error: Could not find {MANIFEST_FILE} in current directory.")
            raise SystemExit(1)

        self.output_dir = self.project_root / 'releases'
        self.manifest = Manifest(self.project_root / MANIFEST_FILE)
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if a path should be excluded from the package."""
        name = path.name
        matches_pattern = any(name.endswith(p[1:]) if p.startswith('*') else name == p for p in self.EXCLUDE_PATTERNS)
        in_hidden_dir = any(part in self.EXCLUDE_PATTERNS for part in path.parts)
        return matches_pattern or in_hidden_dir

    def _clean_zip(self, filepath: Path) -> None:
        """Safe remove existing zip file."""
        if filepath.exists():
            try:
                filepath.unlink()
            except PermissionError:
                print(f"Error: Cannot overwrite {filepath.name}. File might be open.")
                raise SystemExit(1)

    def _add_to_zip(self, zipf: zipfile.ZipFile, source: Path, arcname: Optional[str] = None):
        """Add file or directory to ZIP."""
        if self._should_exclude(source):
            return

        target_name = arcname or source.name
        if source.is_file():
            zipf.write(source, target_name)
        elif source.is_dir():
            for item in source.rglob('*'):
                if not self._should_exclude(item):
                    zipf.write(item, Path(target_name) / item.relative_to(source))

    def _create_package(self, files: List[str], suffix: str = '') -> Path:
        """Common logic for creating a standard package."""
        filename = f'{self.manifest.slug}-v{self.manifest.version}{suffix}.zip'
        filepath = self.output_dir / filename
        self._clean_zip(filepath)
        
        with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item_name in files:
                source = self.project_root / item_name
                if source.exists():
                    self._add_to_zip(zipf, source)
        
        return filepath

    def build_chrome_package(self) -> Path:
        """Create package for Chrome Web Store."""
        return self._create_package(self.CHROME_FILES, '-chrome')
    
    def build_github_package(self) -> Path:
        """Create package for GitHub Release."""
        return self._create_package(self.CHROME_FILES + self.DOCS_FILES)
    
    def build_firefox_package(self, gecko_id: Optional[str] = None) -> Path:
        """Create specialized package for Firefox."""
        filename = f'{self.manifest.slug}-v{self.manifest.version}-firefox.zip'
        filepath = self.output_dir / filename
        self._clean_zip(filepath)

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            
            for item_name in self.CHROME_FILES:
                src = self.project_root / item_name
                dst = tmp_path / item_name
                if not src.exists():
                    continue
                
                if src.is_dir():
                    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*self.EXCLUDE_PATTERNS))
                else:
                    shutil.copy2(src, dst)
            
            firefox_manifest = self.manifest.to_firefox_manifest(gecko_id=gecko_id)
            with open(tmp_path / MANIFEST_FILE, 'w', encoding='utf-8') as f:
                import json
                json.dump(firefox_manifest, f, indent=4, ensure_ascii=False)
            
            with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for item in tmp_path.rglob('*'):
                    if item.is_file():
                        zipf.write(item, item.relative_to(tmp_path))
        
        return filepath
    
    def build_all(self, include_firefox: bool = True, gecko_id: Optional[str] = None) -> Dict[str, Any]:
        """Run all build steps."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        result = {
            'info': {
                'name': self.manifest.name,
                'version': self.manifest.version,
                'description': self.manifest.description,
            },
            'paths': {
                'chrome': self.build_chrome_package(),
                'github': self.build_github_package()
            },
            'output_dir': self.output_dir
        }
        
        if include_firefox:
            result['paths']['firefox'] = self.build_firefox_package(gecko_id=gecko_id)
            
        return result

    @staticmethod
    def format_size(path: Path) -> str:
        """Format file size in human readable format."""
        size = float(path.stat().st_size)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def print_summary(self, result: Dict[str, Any]):
        """Print build summary."""
        print(f"\nBuild Complete: {result['info']['name']} (v{result['info']['version']})")
        print("-" * 60)
        for platform, path in result['paths'].items():
            print(f"{platform.capitalize():<10} : {path.name} ({self.format_size(path)})")
        print("-" * 60)
        print(f"Output     : {result['output_dir']}\n")
