"""Reproducible generator pipeline with a seed manifest (issue #162).

SYNTHETIC DATA ONLY. A run takes a versioned config and a seed, builds the records in memory,
runs every validation check, and only then writes the output and ``seed-manifest.json``.
The same seed and config always give the same file and output digests. The generation
timestamp is recorded in the manifest but is deliberately outside every digest.
"""

import hashlib
import json
import random
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from . import provenance

MANIFEST_NAME = "seed-manifest.json"
SOURCE_TYPE = "SYNTHETIC"

Records = Mapping[str, Sequence[Mapping[str, Any]]]
Generator = Callable[["GeneratorConfig", random.Random], Records]
Validator = Callable[[Records], Sequence[str]]


class PipelineValidationError(ValueError):
    """Raised before any output is written when a validation check reports a failure."""

    def __init__(self, failures: Sequence[str]) -> None:
        self.failures = tuple(failures)
        super().__init__("; ".join(self.failures))


@dataclass(frozen=True)
class GeneratorConfig:
    name: str
    version: str
    seed: int
    as_of: str
    params: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.name or not self.version:
            raise ValueError("config name and version are required")
        if type(self.seed) is not int:
            raise ValueError("seed must be an integer")
        provenance.parse_as_of(self.as_of)

    def digest(self) -> str:
        body = {
            "name": self.name,
            "version": self.version,
            "seed": self.seed,
            "as_of": self.as_of,
            "params": dict(self.params),
        }
        return "sha256:" + hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _render(records: Records) -> dict[str, bytes]:
    """Serialise each dataset as sorted-key JSON lines, in a stable file order."""
    return {
        name: "".join(json.dumps(row, sort_keys=True) + "\n" for row in records[name]).encode()
        for name in sorted(records)
    }


def output_digest(files: Mapping[str, bytes]) -> str:
    """Digest of file names and exact bytes, independent of the manifest and timestamp."""
    digest = hashlib.sha256()
    for name in sorted(files):
        for part in (name.encode("utf-8"), files[name]):
            digest.update(len(part).to_bytes(8, "big"))
            digest.update(part)
    return "sha256:" + digest.hexdigest()


def build(
    config: GeneratorConfig, generate: Generator, validators: Sequence[Validator] = ()
) -> dict[str, bytes]:
    """Generate and validate in memory; raise PipelineValidationError before any write."""
    config.validate()
    records = generate(config, random.Random(f"{config.name}:{config.version}:{config.seed}"))
    if not records or any(not name or "/" in name or "\\" in name for name in records):
        raise PipelineValidationError(["generator must return named datasets"])
    failures = [message for check in validators for message in check(records)]
    if failures:
        raise PipelineValidationError(failures)
    return _render(records)


def run(
    config: GeneratorConfig,
    generate: Generator,
    out: str | Path,
    *,
    validators: Sequence[Validator] = (),
    clock: Callable[[], datetime] | None = None,
) -> dict[str, Any]:
    files = build(config, generate, validators)
    generated_at = (clock or (lambda: datetime.now(UTC)))()
    if generated_at.tzinfo is None:
        raise ValueError("generation timestamp must be timezone-aware")
    destination = provenance.prepare_output(out)
    for name, payload in files.items():
        (destination / name).write_bytes(payload)
    manifest = {
        "generator": config.name,
        "config_version": config.version,
        "config_sha256": config.digest(),
        "seed": config.seed,
        "as_of": config.as_of,
        "generated_at": generated_at.astimezone(UTC).isoformat(),
        "file_sha256": provenance.file_hashes(destination / name for name in files),
        "output_sha256": output_digest(files),
        "validation_checks": len(validators),
        "source_type": SOURCE_TYPE,
    }
    (destination / MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    return manifest


def verify(
    out: str | Path,
    config: GeneratorConfig,
    generate: Generator,
    validators: Sequence[Validator] = (),
) -> list[str]:
    """Regenerate from the config and compare with the written output; return the differences."""
    directory = Path(out)
    manifest = json.loads((directory / MANIFEST_NAME).read_text(encoding="utf-8"))
    expected = build(config, generate, validators)
    problems = []
    for key, value in (
        ("seed", config.seed),
        ("config_version", config.version),
        ("config_sha256", config.digest()),
        ("output_sha256", output_digest(expected)),
    ):
        if manifest.get(key) != value:
            problems.append(f"manifest {key} differs from the regenerated run")
    if not manifest.get("generated_at"):
        problems.append("manifest generated_at is missing")
    actual = {p.name for p in directory.iterdir() if p.name != MANIFEST_NAME}
    if actual != set(expected):
        problems.append("output file set differs from the regenerated run")
    for name, payload in expected.items():
        path = directory / name
        if path.is_file() and path.read_bytes() != payload:
            problems.append(f"{name} bytes differ from the regenerated run")
        recorded = manifest.get("file_sha256", {}).get(name)
        if recorded != hashlib.sha256(payload).hexdigest():
            problems.append(f"{name} digest differs from the manifest")
    return problems
