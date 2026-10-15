"""SYNTHETIC DATA ONLY. Shared manifest helpers for reproducible generator runs.

The generator revision is a SHA-256 over the generator source files, so it is
stable across checkouts and never depends on the clock or on Git metadata.
"""
import hashlib
import os
from zava_forward.core.synthetic import stock_fabric

HERE = os.path.dirname(os.path.abspath(__file__))


def generator_revision():
    digest = hashlib.sha256()
    for name in sorted(os.listdir(HERE)):
        if name.endswith(".py"):
            digest.update(name.encode())
            with open(os.path.join(HERE, name), "rb") as f:
                digest.update(f.read())
    for path in sorted(stock_fabric.revision_sources(), key=lambda path: path.name):
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return "sha256:" + digest.hexdigest()[:16]


def file_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()
