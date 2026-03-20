"""Manifest handling for browser extensions."""

import json
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


class Manifest:
    """Represents the extension manifest.json file."""

    def __init__(self, path: Path):
        """Load manifest from file."""
        self.path = path
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        """Read and parse manifest.json."""
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading manifest at {self.path}: {e}")
            raise SystemExit(1)

    def _save(self) -> None:
        """Write manifest.json back to disk."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=4, ensure_ascii=False)
            f.write("\n")

    @property
    def name(self) -> str:
        """Extension name."""
        return self._data.get("name", "extension")

    @property
    def slug(self) -> str:
        """URL-friendly name (lowercase, hyphenated)."""
        name = self.name.lower()
        name = re.sub(r"[^a-z0-9]+", "-", name)
        return name.strip("-")

    @property
    def version(self) -> str:
        """Extension version."""
        return self._data.get("version", "0.0.0")

    @version.setter
    def version(self, value: str):
        """Set extension version and save."""
        self._data["version"] = value
        self._save()

    @property
    def description(self) -> str:
        """Extension description."""
        return self._data.get("description", "")

    def get(self, key: str, default: Any = None) -> Any:
        """Get any manifest property."""
        return self._data.get(key, default)

    def to_firefox_manifest(self, gecko_id: Optional[str] = None) -> Dict[str, Any]:
        """Convert Chrome manifest to Firefox-compatible format."""
        import copy

        firefox_data = copy.deepcopy(self._data)

        if "background" in firefox_data:
            bg = firefox_data["background"]
            if "service_worker" in bg:
                script_path = bg.pop("service_worker")
                bg["scripts"] = [script_path]

        b_settings = firefox_data.get("browser_specific_settings", {})
        gecko = b_settings.get("gecko", {})

        final_id = gecko_id or gecko.get("id") or f"{self.slug}@fastfingertips"

        firefox_data["browser_specific_settings"] = {
            "gecko": {
                "id": final_id,
                "strict_min_version": gecko.get("strict_min_version", "109.0"),
            }
        }

        return firefox_data

    def bump_version(self, bump_type: str = "patch") -> Tuple[str, str]:
        """Increment version number."""
        old_version = self.version
        parts = old_version.split(".")

        while len(parts) < 3:
            parts.append("0")

        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1

        new_version = f"{major}.{minor}.{patch}"
        self.version = new_version

        return old_version, new_version
