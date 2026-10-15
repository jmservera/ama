"""Reproducibility metadata and non-destructive destinations for synthetic tools."""

import hashlib
from collections.abc import Iterable
from datetime import date
from pathlib import Path


def parse_as_of(value: str) -> date:
    """Parse an explicit ISO calendar date without accepting compact/week dates."""
    parsed = date.fromisoformat(value)
    if parsed.isoformat() != value:
        raise ValueError("as_of must use YYYY-MM-DD")
    return parsed


def source_revision(sources: Iterable[Path]) -> str:
    """Fingerprint named generator dependencies, independent of their physical roots."""
    files = sorted(sources, key=lambda p: p.name)
    if len({p.name for p in files}) != len(files):
        raise ValueError("Generator source basenames must be unique")
    digest = hashlib.sha256()
    for path in files:
        for part in (path.name.encode("utf-8"), path.read_bytes()):
            digest.update(len(part).to_bytes(8, "big"))
            digest.update(part)
    return "sha256:" + digest.hexdigest()


def prepare_output(out: str | Path) -> Path:
    """Create a new/empty destination; never replace a previous exercise snapshot."""
    path = Path(out)
    if path.is_symlink():
        raise FileExistsError(f"Refusing symlink output {path}; choose a new snapshot directory")
    path.mkdir(parents=True, exist_ok=True)
    if any(path.iterdir()):
        raise FileExistsError(f"Output {path} is not empty; choose a new snapshot directory")
    return path


def file_hashes(files: Iterable[Path]) -> dict[str, str]:
    """Hash exact payload bytes, excluding the manifest that will contain the hashes."""
    hashes = {}
    for path in sorted(files):
        with path.open("rb") as payload:
            hashes[path.name] = hashlib.file_digest(payload, "sha256").hexdigest()
    return hashes
