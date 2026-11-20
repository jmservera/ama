"""Scan git-tracked files for high-confidence secret values (Issue #138, criterion 6)."""

import re
import subprocess
import sys
from pathlib import Path

RULES = {
    "private-key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "aws-access-key-id": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github-token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{40,})"),
    "azure-storage-key": re.compile(r"AccountKey=[A-Za-z0-9+/=]{20,}"),
    "sas-signature": re.compile(r"[?&]sig=[A-Za-z0-9%+/=]{30,}"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}"),
    "connection-string-password": re.compile(r"(?i)\b(?:password|pwd)=[^;\"'\s$<{]{6,};"),
}

# Synthetic fixtures that deliberately contain a secret-shaped value to test redaction.
ALLOWLIST = {
    ("src/api/tests/test_iot_credential_hygiene.py", "private-key"),
    ("src/core/tests/test_assistants_identity.py", "aws-access-key-id"),
    ("src/core/tests/test_diagnostic_logging.py", "azure-storage-key"),
    ("src/core/tests/test_sqlstore.py", "connection-string-password"),
}


def scan_text(path: str, text: str) -> list[tuple[str, int, str]]:
    """Return (path, line number, rule) for each non-allowlisted match."""
    findings = []
    for number, line in enumerate(text.splitlines(), start=1):
        for rule, pattern in RULES.items():
            if pattern.search(line) and (path, rule) not in ALLOWLIST:
                findings.append((path, number, rule))
    return findings


def scan_repo(root: Path) -> list[tuple[str, int, str]]:
    listing = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"], capture_output=True, check=True
    ).stdout
    findings = []
    for name in listing.decode().split("\0"):
        path = root / name
        if not name or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        findings.extend(scan_text(name, text))
    return findings


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    findings = scan_repo(root)
    for path, number, rule in findings:
        print(f"{path}:{number}: {rule}")
    print(f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
