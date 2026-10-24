#!/usr/bin/env python3
"""Bounded PR438 preservation. Build, verify and restore do not delete sources.

Usage: .venv/bin/python tools/tracking_retention.py build --repo .
Prune is a separate, explicitly confirmed action after promotion and review.
Symlink targets are opaque archive data, never opened or restored.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tarfile
import tempfile
from typing import Any, BinaryIO, Iterator

TRACKING = ".copilot-tracking"
MANIFEST = "docs/reference/resources/tracking-retention-manifest.json"
EXPECTED_BYTES = 26_219_104
ARCHIVE_BASE = Path.home() / ".local/share/ama/tracking-archives"
CANONICAL = {
    "docs/capstone/deck/zava-forward-cowork-v2-draft.pptx":
        "39659a3ad9974f802a8418177a9ca0ca8daf7478e71cd82d04cd7677d9ad2cc0",
    "docs/capstone/deck/zava-forward-cowork-v2-draft.pdf":
        "b816f3f2282ffad4e0afd41cc39ba76a6871bc62c2292c5a62129a4864bd9a9c",
}


class RetentionError(Exception):
    """A failed preservation prerequisite; no broadened cleanup is permitted."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RetentionError(message)


def approved_paths() -> tuple[str, ...]:
    """Expand only the seven finite D2 rows and D1a/b in the approved report."""
    groups = {
        "2026-09-11/proper-warm-cxo-introduction/final/preview":
            [f"Slide{number}.PNG" for number in range(1, 15)] + ["overview.png"],
        "2026-09-11/proper-warm-cxo-introduction/slide-deck/preview":
            [f"Slide{number}.PNG" for number in range(1, 13)] + ["overview.png"],
        "2026-09-18/proper-warm-cxo/slide-deck/validation":
            [f"Slide{number}.JPG" for number in range(1, 12)]
            + ["contact-sheet.jpg", "corrected-slides.jpg"],
        "2026-09-26/ama-mentor-progress-review/slide-deck/validation":
            [f"slide-{number:03}.jpg" for number in range(1, 16)],
        "2026-10-13/zava-forward-agent-process/slide-deck/validation":
            [f"parent-slide-{number}.jpg" for number in range(12, 15)],
        "2026-10-14/zava-forward-architecture-refresh/slide-deck/validation":
            [f"slide-{number:03}.jpg" for number in range(1, 25)]
            + ["contact-01-06.jpg", "contact-07-12.jpg", "contact-13-18.jpg", "contact-19-24.jpg"],
        "2026-10-14/zava-forward-capstone-rebuild/slide-deck/validation":
            [f"slide-{number:03}.jpg" for number in range(1, 23)]
            + ["contact-01-06.jpg", "contact-07-12.jpg", "contact-13-18.jpg", "contact-19-22.jpg"],
    }
    paths = [f"{TRACKING}/ppt/{directory}/{name}"
             for directory, names in groups.items() for name in names]
    paths += [
        f"{TRACKING}/ppt/2026-09-26/ama-mentor-progress-review/slide-deck/ama-mentor-progress-review.pptx",
        f"{TRACKING}/ppt/2026-10-14/zava-forward-architecture-refresh/slide-deck/zava-forward-executive-draft.pptx",
    ]
    return tuple(sorted(paths))


def safe_parts(name: str) -> tuple[str, ...]:
    parts = PurePosixPath(name).parts
    require(bool(parts) and not name.startswith("/") and "\\" not in name
            and all(part not in ("", ".", "..") for part in name.split("/"))
            and "\x00" not in name, "Unsafe member path")
    return parts


@contextmanager
def parent_fd(root: Path, name: str) -> Iterator[tuple[int, str]]:
    parts = safe_parts(name)
    descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        yield descriptor, parts[-1]
    finally:
        os.close(descriptor)


def restore_parents(root: Path, name: str) -> None:
    descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in safe_parts(name)[:-1]:
            try:
                os.mkdir(part, mode=0o700, dir_fd=descriptor)
            except FileExistsError:
                pass
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
    finally:
        os.close(descriptor)


def digest(stream: BinaryIO) -> str:
    result = hashlib.sha256()
    while block := stream.read(1024 * 1024):
        result.update(block)
    return result.hexdigest()


def fingerprint(info: os.stat_result) -> list[int]:
    return [info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_nlink]


@contextmanager
def regular(root: Path, name: str) -> Iterator[BinaryIO]:
    with parent_fd(root, name) as (directory, leaf):
        descriptor = os.open(leaf, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                             dir_fd=directory)
        with os.fdopen(descriptor, "rb") as stream:
            before = os.fstat(stream.fileno())
            require(stat.S_ISREG(before.st_mode) and bool(before.st_mode & 0o444),
                    "Not a readable regular file")
            yield stream
            after = os.stat(leaf, dir_fd=directory, follow_symlinks=False)
            require(fingerprint(before) == fingerprint(after)
                    == fingerprint(os.fstat(stream.fileno())), "Source changed during read")


def entry_at(directory: int, leaf: str, name: str) -> dict[str, Any]:
    info = os.stat(leaf, dir_fd=directory, follow_symlinks=False)
    entry: dict[str, Any] = {"path": name, "mode": stat.S_IMODE(info.st_mode),
                             "fingerprint": fingerprint(info)}
    if stat.S_ISLNK(info.st_mode):
        target = os.readlink(leaf, dir_fd=directory)
        raw = os.fsencode(target)
        entry.update(type="symlink", size=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    elif stat.S_ISDIR(info.st_mode):
        require(bool(info.st_mode & 0o444) and bool(info.st_mode & 0o111),
                "Unreadable directory")
        entry.update(type="directory", size=0)
    elif stat.S_ISREG(info.st_mode):
        require(bool(info.st_mode & 0o444), "Unreadable file")
        descriptor = os.open(leaf, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                             dir_fd=directory)
        with os.fdopen(descriptor, "rb") as stream:
            require(fingerprint(os.fstat(stream.fileno())) == fingerprint(info),
                    "Source identity changed")
            entry.update(type="file", size=info.st_size, sha256=digest(stream))
            require(fingerprint(os.fstat(stream.fileno())) == fingerprint(info),
                    "Source changed during inventory")
    else:
        raise RetentionError("Special filesystem entry refused")
    require(fingerprint(os.stat(leaf, dir_fd=directory, follow_symlinks=False))
            == fingerprint(info), "Source changed during inventory")
    return entry


def inventory(repo: Path) -> list[dict[str, Any]]:
    """Snapshot every directory, file and opaque link without following links."""
    entries: list[dict[str, Any]] = []

    def visit(directory: int, leaf: str, name: str) -> None:
        safe_parts(name)
        entry = entry_at(directory, leaf, name)
        entries.append(entry)
        if entry["type"] == "directory":
            child = os.open(leaf, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=directory)
            try:
                require(fingerprint(os.fstat(child)) == entry["fingerprint"],
                        "Directory identity changed")
                for item in sorted(os.listdir(child)):
                    visit(child, item, f"{name}/{item}")
                require(fingerprint(os.fstat(child)) == entry["fingerprint"],
                        "Directory changed during inventory")
            finally:
                os.close(child)

    with parent_fd(repo, TRACKING) as (directory, leaf):
        visit(directory, leaf, TRACKING)
    return sorted(entries, key=lambda entry: entry["path"])


def identity(entry: dict[str, Any]) -> dict[str, Any]:
    return {key: entry[key] for key in ("path", "type", "size", "sha256") if key in entry}


def selected(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    indexed = {entry["path"]: entry for entry in entries}
    result = [identity(indexed[name]) for name in approved_paths() if name in indexed]
    require(tuple(entry["path"] for entry in result) == approved_paths(),
            "Missing approved member")
    require(all(entry["type"] == "file" for entry in result), "Selection must be regular files")
    require(sum(entry["size"] for entry in result) == EXPECTED_BYTES, "Selection byte total changed")
    return result


def portable(path: Path) -> str:
    try:
        return "~/" + path.relative_to(Path.home()).as_posix()
    except ValueError:
        return str(path)


def external(path: Path, repo: Path) -> Path:
    path = path.expanduser().absolute()
    require(".." not in path.parts, "External path traversal refused")
    require(not path.is_relative_to(repo.resolve()), "Output must be outside repository")
    for component in (path, *path.parents):
        require(not component.is_symlink(), "External path contains a symlink")
    return path


def private(path: Path, directory: bool = False) -> None:
    info = path.lstat()
    require(info.st_uid == os.getuid()
            and stat.S_IMODE(info.st_mode) == (0o700 if directory else 0o600)
            and (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)),
            "Archive permissions or ownership invalid")


def write_json(path: Path, value: Any, mode: int = 0o600) -> None:
    with path.open("x", encoding="utf-8") as stream:
        path.chmod(mode)
        json.dump(value, stream, separators=(",", ":"), ensure_ascii=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def read_json(path: Path) -> Any:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, "Duplicate JSON key")
            result[key] = value
        return result

    with path.open(encoding="utf-8") as stream:
        return json.load(stream, object_pairs_hook=unique)


def file_hash(path: Path) -> str:
    with regular(path.parent, path.name) as stream:
        return digest(stream)


def canonical_hashes(repo: Path) -> dict[str, str]:
    result = {}
    for name, expected in CANONICAL.items():
        with regular(repo, name) as stream:
            result[name] = digest(stream)
        require(result[name] == expected, "Canonical deck hash changed")
    return result


def verify_archive(archive: Path, entries: list[dict[str, Any]]) -> None:
    indexed = {entry["path"]: entry for entry in entries}
    require(len(indexed) == len(entries), "Duplicate inventory member")
    seen: set[str] = set()
    for name in indexed:
        require(safe_parts(name)[0] == TRACKING, "Member outside tracking")
        for parent in PurePosixPath(name).parents:
            if str(parent) != ".":
                require(str(parent) in indexed and indexed[str(parent)]["type"] == "directory",
                        "Unsafe member ancestor")
    with tarfile.open(archive, "r:gz") as bundle:
        for member in bundle:
            safe_parts(member.name)
            require(member.name in indexed and member.name not in seen,
                    "Unexpected or duplicate archive member")
            seen.add(member.name)
            entry = indexed[member.name]
            require(member.mode == entry["mode"], "Member mode mismatch")
            if entry["type"] == "file":
                require(member.isfile() and member.size == entry["size"], "Member type/size mismatch")
                stream = bundle.extractfile(member)
                require(stream is not None, "Missing member bytes")
                with stream:
                    require(digest(stream) == entry["sha256"], "Member checksum mismatch")
            elif entry["type"] == "directory":
                require(member.isdir() and member.size == 0, "Member directory mismatch")
            else:
                require(entry["type"] == "symlink" and member.issym() and member.size == 0,
                        "Unsafe archive type")
                target = os.fsencode(member.linkname)
                require(len(target) == entry["size"]
                        and hashlib.sha256(target).hexdigest() == entry["sha256"],
                        "Link identity mismatch")
    require(seen == set(indexed), "Missing archive member")


class Retention:
    """Fixed-scope archive workflow. No runtime selection override exists."""

    def __init__(self, repo: Path) -> None:
        self.repo = repo.resolve(strict=True)
        self.manifest = self.repo / MANIFEST

    def build(self) -> dict[str, Any]:
        require(not self.manifest.exists() and not self.manifest.is_symlink(),
                "Manifest already exists; refusing overwrite")
        decks = canonical_hashes(self.repo)
        entries = inventory(self.repo)
        removal = selected(entries)
        base = external(ARCHIVE_BASE, self.repo)
        base.mkdir(parents=True, mode=0o700, exist_ok=True)
        base.chmod(0o700)
        destination = Path(tempfile.mkdtemp(prefix="2026-10-24-pr438-", dir=base))
        destination.chmod(0o700)
        archive = destination / "tracking.tar.gz"
        with archive.open("xb") as output:
            archive.chmod(0o600)
            with tarfile.open(fileobj=output, mode="w:gz", dereference=False) as bundle:
                for entry in entries:
                    name = entry["path"]
                    member = tarfile.TarInfo(name)
                    member.mode = entry["mode"]
                    member.mtime = entry["fingerprint"][3] / 1_000_000_000
                    if entry["type"] == "file":
                        member.size = entry["size"]
                        with regular(self.repo, name) as stream:
                            require(digest(stream) == entry["sha256"], "Source drift before archive")
                            stream.seek(0)
                            bundle.addfile(member, stream)
                    elif entry["type"] == "directory":
                        member.type = tarfile.DIRTYPE
                        bundle.addfile(member)
                    else:
                        member.type = tarfile.SYMTYPE
                        with parent_fd(self.repo, name) as (directory, leaf):
                            member.linkname = os.readlink(leaf, dir_fd=directory)
                        require(hashlib.sha256(os.fsencode(member.linkname)).hexdigest()
                                == entry["sha256"], "Link drift before archive")
                        bundle.addfile(member)
            output.flush()
            os.fsync(output.fileno())
        require(inventory(self.repo) == entries, "Tracking changed during archive; retry explicitly")
        require(canonical_hashes(self.repo) == decks, "Canonical drift")
        verify_archive(archive, entries)
        counts = {kind: sum(entry["type"] == kind for entry in entries)
                  for kind in ("file", "symlink", "directory")}
        counts["logical_file_bytes"] = sum(entry["size"] for entry in entries if entry["type"] == "file")
        counts["allocated_bytes"] = sum(
            os.stat(self.repo / entry["path"], follow_symlinks=False).st_blocks * 512
            for entry in entries)
        receipt = {"schema": 1, "archive_sha256": file_hash(archive), "inventory": entries,
                   "before": counts, "canonical": decks,
                   "git_status": subprocess.check_output(
                       ["git", "-C", str(self.repo), "status", "--short"], text=True),
                   "branch": subprocess.check_output(
                       ["git", "-C", str(self.repo), "branch", "--show-current"], text=True).strip()}
        receipt_path = destination / "receipt.json"
        write_json(receipt_path, receipt)
        compact = {"schema": 1, "external_directory": portable(destination),
                   "archive": "tracking.tar.gz", "receipt": "receipt.json",
                   "archive_sha256": receipt["archive_sha256"],
                   "receipt_sha256": file_hash(receipt_path), "before": counts,
                   "archive_bytes": archive.stat().st_size, "canonical": decks,
                   "selected_count": len(removal), "selected_bytes": EXPECTED_BYTES,
                   "selected": removal}
        self.manifest.parent.mkdir(parents=True, exist_ok=True)
        write_json(self.manifest, compact, 0o644)
        return compact

    def verify(self) -> tuple[dict[str, Any], dict[str, Any], Path]:
        require(not self.manifest.is_symlink(), "Manifest symlink refused")
        compact = read_json(self.manifest)
        require(compact["schema"] == 1 and compact["archive"] == "tracking.tar.gz"
                and compact["receipt"] == "receipt.json", "Invalid receipt schema")
        destination = external(Path(compact["external_directory"]), self.repo)
        private(destination, directory=True)
        archive = destination / "tracking.tar.gz"
        receipt_path = destination / "receipt.json"
        private(archive)
        private(receipt_path)
        require(file_hash(receipt_path) == compact["receipt_sha256"], "Receipt checksum mismatch")
        receipt = read_json(receipt_path)
        require(file_hash(archive) == compact["archive_sha256"] == receipt["archive_sha256"],
                "Archive checksum mismatch")
        require(compact["selected"] == selected(receipt["inventory"])
                and compact["selected_count"] == len(approved_paths())
                and compact["selected_bytes"] == EXPECTED_BYTES, "Out-of-set or altered manifest")
        require(compact["before"] == receipt["before"]
            and compact["archive_bytes"] == archive.stat().st_size,
            "Manifest accounting mismatch")
        require(compact["canonical"] == receipt["canonical"] == canonical_hashes(self.repo),
                "Canonical receipt mismatch")
        verify_archive(archive, receipt["inventory"])
        return compact, receipt, destination

    def restore(self, output: Path) -> dict[str, Any]:
        compact, _, destination = self.verify()
        output = external(output, self.repo)
        require(not output.exists() and not output.is_symlink(),
                "Restore requires a new empty external directory")
        output.mkdir(mode=0o700)
        with tarfile.open(destination / "tracking.tar.gz", "r:gz") as bundle:
            for entry in compact["selected"]:
                restore_parents(output, entry["path"])
                with parent_fd(output, entry["path"]) as (directory, leaf):
                    descriptor = os.open(leaf, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                         0o600, dir_fd=directory)
                    source = bundle.extractfile(entry["path"])
                    require(source is not None, "Missing restore member")
                    with source, os.fdopen(descriptor, "wb") as stream:
                        while block := source.read(1024 * 1024):
                            stream.write(block)
                        stream.flush()
                        os.fsync(stream.fileno())
                self.check_file(output, entry)
        proof = {"archive_sha256": compact["archive_sha256"],
                 "receipt_sha256": compact["receipt_sha256"],
                 "restore_directory": portable(output), "verified": compact["selected"],
                 "count": len(compact["selected"]), "bytes": EXPECTED_BYTES}
        write_json(output / "restore-proof.json", proof)
        return proof

    @staticmethod
    def check_file(root: Path, entry: dict[str, Any]) -> None:
        with regular(root, entry["path"]) as stream:
            require(os.fstat(stream.fileno()).st_size == entry["size"]
                    and digest(stream) == entry["sha256"], "Selected source drift")

    def protected(self, receipt: dict[str, Any]) -> None:
        """Compare pre-existing protected identities, allowing new task records."""
        current = {entry["path"]: identity(entry) for entry in inventory(self.repo)}
        for entry in receipt["inventory"]:
            if entry["path"] not in approved_paths():
                require(current.get(entry["path"]) == identity(entry), "Protected tracking content changed")

    def prune(self, proof_path: Path, *, recover: bool = False) -> list[str]:
        compact, receipt, destination = self.verify()
        proof_path = external(proof_path, self.repo)
        private(proof_path)
        proof = read_json(proof_path)
        require(proof["archive_sha256"] == compact["archive_sha256"]
                and proof["receipt_sha256"] == compact["receipt_sha256"]
                and proof["verified"] == compact["selected"], "Restore proof mismatch")
        restored = external(Path(proof["restore_directory"]), self.repo)
        for entry in compact["selected"]:
            self.check_file(restored, entry)
        self.protected(receipt)
        journal = destination / "prune-journal.jsonl"
        done: set[str] = set()
        pending: str | None = None
        header = {"archive_sha256": compact["archive_sha256"],
                  "receipt_sha256": compact["receipt_sha256"]}
        require(recover == journal.exists(), "Existing journal requires --recover; recovery requires journal")
        if recover:
            private(journal)
            with journal.open(encoding="utf-8") as stream:
                require(json.loads(next(stream)) == header, "Journal identity mismatch")
                for line in stream:
                    event = json.loads(line)
                    name = event["path"]
                    require(name in approved_paths() and name not in done, "Out-of-set journal")
                    if event["event"] == "pending":
                        require(pending is None, "Invalid pending journal")
                        pending = name
                    else:
                        require(event["event"] == "removed" and pending == name,
                                "Invalid removal journal")
                        done.add(name)
                        pending = None
        for entry in compact["selected"]:
            name = entry["path"]
            with parent_fd(self.repo, name) as (directory, leaf):
                exists = True
                try:
                    os.stat(leaf, dir_fd=directory, follow_symlinks=False)
                except FileNotFoundError:
                    exists = False
            if name in done:
                require(not exists, "Removed path unexpectedly exists")
            elif recover and name == pending and not exists:
                continue
            else:
                self.check_file(self.repo, entry)
        with journal.open("a" if recover else "x", encoding="utf-8") as stream:
            journal.chmod(0o600)

            def record(value: dict[str, Any]) -> None:
                stream.write(json.dumps(value, separators=(",", ":")) + "\n")
                stream.flush()
                os.fsync(stream.fileno())

            if not recover:
                record(header)
            for entry in compact["selected"]:
                name = entry["path"]
                if name in done:
                    continue
                if name != pending:
                    record({"event": "pending", "path": name})
                with parent_fd(self.repo, name) as (directory, leaf):
                    try:
                        info = os.stat(leaf, dir_fd=directory, follow_symlinks=False)
                    except FileNotFoundError:
                        require(recover and name == pending, "Unexpected missing selected path")
                    else:
                        self.check_file(self.repo, entry)
                        require(fingerprint(os.stat(leaf, dir_fd=directory, follow_symlinks=False))
                                == fingerprint(info), "Identity changed before removal")
                        os.unlink(leaf, dir_fd=directory)
                        os.fsync(directory)
                record({"event": "removed", "path": name})
                done.add(name)
                pending = None
        self.protected(receipt)
        canonical_hashes(self.repo)
        return sorted(done)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("build", "verify", "restore", "prune", "check-protected"))
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, help="New external restore directory")
    parser.add_argument("--restore-proof", type=Path)
    parser.add_argument("--confirm-prune", action="store_true")
    parser.add_argument("--recover", action="store_true")
    return parser


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()
    try:
        operation = Retention(args.repo)
        if args.action == "build":
            result = operation.build()
            print(json.dumps({key: result[key] for key in (
                "external_directory", "archive_sha256", "archive_bytes", "before",
                "selected_count", "selected_bytes")}))
        elif args.action == "restore":
            require(args.output is not None, "--output required")
            result = operation.restore(args.output)
            print(json.dumps({key: result[key] for key in ("restore_directory", "count", "bytes")}))
        elif args.action == "prune":
            require(args.confirm_prune and args.restore_proof is not None,
                    "Prune requires --confirm-prune and --restore-proof")
            removed = operation.prune(args.restore_proof, recover=args.recover)
            print(json.dumps({"removed_count": len(removed), "removed_bytes": EXPECTED_BYTES}))
        else:
            _, receipt, _ = operation.verify()
            if args.action == "check-protected":
                operation.protected(receipt)
            print("PASS: full archive readback" + (
                " and protected snapshot comparison" if args.action == "check-protected" else ""))
        return 0
    except KeyboardInterrupt:
        print("Interrupted; retain archive and journal; use explicit recovery after inspection.", file=sys.stderr)
        return 130
    except RetentionError as error:
        print(f"FAILED: {error}; no broader cleanup authorized.", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError, StopIteration, tarfile.TarError) as error:
        print(f"FAILED: {type(error).__name__}; inspect local inputs. "
              "Paths and link targets are intentionally not printed.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())