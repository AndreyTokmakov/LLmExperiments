from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple


class FileManager:
    """Fail-safe file manager (no exceptions raised)."""

    @staticmethod
    def read_file(path: str) -> Tuple[Optional[str], Optional[str]]:
        """Read file content.

        Returns:
            (data, error)
        """
        try:
            p = Path(path)

            if not p.exists():
                return None, f"File not found: {path}"
            if not p.is_file():
                return None, f"Path is not a file: {path}"

            return p.read_text(encoding="utf-8"), None

        except Exception as e:
            return None, str(e)

    @staticmethod
    def write_file(path: str, data: str) -> Tuple[bool, Optional[str]]:
        """Write text to file.

        Returns:
            (success, error)
        """
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(data, encoding="utf-8")
            return True, None

        except Exception as e:
            return False, str(e)

    @staticmethod
    def list_files(path: str, recursive: bool = False) -> Tuple[List[str], Optional[str]]:
        """List files in directory.

        Returns:
            (files, error)
        """
        try:
            p = Path(path)

            if not p.exists():
                return [], f"Directory not found: {path}"
            if not p.is_dir():
                return [], f"Path is not a directory: {path}"

            if recursive:
                files = [str(f) for f in p.rglob("*") if f.is_file()]
            else:
                files = [str(f) for f in p.iterdir() if f.is_file()]

            files = [f.replace(path + '/', '') for f in files]
            return files, None

        except Exception as e:
            return [], str(e)