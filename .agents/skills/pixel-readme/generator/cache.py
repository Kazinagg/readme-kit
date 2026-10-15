"""
Incremental Build Cache for Pixel Readme Kit v4.0
Tracks directive hashes and generated SVG files to skip redundant generation
and preserve file modification timestamps.
"""

import os
import json
import hashlib

CACHE_FILE_DEFAULT = ".pixel-cache.json"

class BuildCache:
    def __init__(self, cache_file=CACHE_FILE_DEFAULT, enabled=True):
        self.cache_file = cache_file
        self.enabled = enabled
        self.entries = {}
        self._dirty = False
        self._load()

    def _load(self):
        if not self.enabled or not os.path.exists(self.cache_file):
            self.entries = {}
            return

        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self.entries = data.get("entries", {})
                else:
                    self.entries = {}
        except Exception:
            self.entries = {}

    def compute_hash(self, obj) -> str:
        """Computes deterministic SHA-256 hash of a serializable object or string."""
        if isinstance(obj, (str, bytes)):
            raw = obj if isinstance(obj, bytes) else obj.encode("utf-8")
        else:
            try:
                raw = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
            except Exception:
                raw = str(obj).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def is_valid(self, filepath: str, content_hash: str) -> bool:
        """
        Returns True if the file exists on disk, has non-zero size,
        and its cached hash matches content_hash.
        """
        if not self.enabled:
            return False

        norm_path = os.path.normpath(filepath).replace("\\", "/")
        entry = self.entries.get(norm_path)
        if not entry:
            return False

        if entry.get("hash") != content_hash:
            return False

        if not os.path.exists(filepath):
            return False

        try:
            if os.path.getsize(filepath) == 0:
                return False
        except OSError:
            return False

        return True

    def record(self, filepath: str, content_hash: str):
        """Records a successful build of a file with its content hash."""
        if not self.enabled:
            return

        norm_path = os.path.normpath(filepath).replace("\\", "/")
        try:
            mtime = os.path.getmtime(filepath)
            size = os.path.getsize(filepath)
        except OSError:
            mtime = 0
            size = 0

        self.entries[norm_path] = {
            "hash": content_hash,
            "mtime": mtime,
            "size": size
        }
        self._dirty = True

    def remove(self, filepath: str):
        """Removes a file entry from cache."""
        norm_path = os.path.normpath(filepath).replace("\\", "/")
        if norm_path in self.entries:
            del self.entries[norm_path]
            self._dirty = True

    def get_known_files(self) -> set:
        """Returns all tracked normalized filepaths in cache."""
        return set(self.entries.keys())

    def save(self):
        """Persists cache to disk if modified."""
        if not self.enabled or not self._dirty:
            return

        data = {
            "version": "4.0",
            "entries": self.entries
        }
        try:
            os.makedirs(os.path.dirname(os.path.abspath(self.cache_file)), exist_ok=True)
            temp_file = f"{self.cache_file}.tmp"
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            if os.path.exists(self.cache_file):
                os.replace(temp_file, self.cache_file)
            else:
                os.rename(temp_file, self.cache_file)
            self._dirty = False
        except Exception:
            pass
