"""Check that deployed demo images trace to commits that build from `src/` (Issue #203, criterion 5).

An image tagged `<repo>:demo-<sha>` is accepted only when `<sha>` exists, is an
ancestor of `--ref`, contains the Dockerfile named by `--dockerfile` and has no
retired `mvp/` or `prototype/` tree (archive tag v0.21.0). The tag is the publisher's assertion, not a
build attestation. Digest-pinned references carry no commit and are reported as
unverifiable.

Exit codes: 0 all verified, 1 any failure, 2 unverifiable and none failed.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

TAG = re.compile(r"^(?P<repo>[^@]+):demo-(?P<sha>[0-9a-f]{7,40})$")
RETIRED_TREES = ("mvp", "prototype")


def git_ok(root: Path, *args: str) -> bool:
    return (
        subprocess.run(["git", *args], check=False, cwd=root, capture_output=True).returncode == 0
    )


def tree_entries(root: Path, sha: str) -> set[str]:
    out = subprocess.run(
        ["git", "ls-tree", "--name-only", sha],
        check=False,
        cwd=root,
        capture_output=True,
        text=True,
    )
    return set(out.stdout.split())


def check_image(root: Path, image: str, ref: str, dockerfile: str) -> tuple[str, str]:
    """Return (status, detail) where status is verified, failed or unverifiable."""
    match = TAG.match(image)
    if not match:
        return "unverifiable", "no demo-<sha> tag (digest-pinned or other tag)"
    sha = match["sha"]
    if not git_ok(root, "cat-file", "-e", f"{sha}^{{commit}}"):
        return "failed", f"commit {sha} not found"
    if not git_ok(root, "merge-base", "--is-ancestor", sha, ref):
        return "failed", f"commit {sha} is not an ancestor of {ref}"
    if not git_ok(root, "cat-file", "-e", f"{sha}:{dockerfile}"):
        return "failed", f"{dockerfile} absent at {sha}"
    retired = sorted(set(RETIRED_TREES) & tree_entries(root, sha))
    if retired:
        return "failed", f"retired tree present at {sha}: {', '.join(retired)}"
    return "verified", f"{sha} is an ancestor of {ref}, has {dockerfile}, no retired tree"


def image_from_azure(resource_group: str, app: str) -> str:
    out = subprocess.run(
        [
            "az",
            "containerapp",
            "show",
            "-g",
            resource_group,
            "-n",
            app,
            "--query",
            "properties.template.containers[0].image",
            "-o",
            "tsv",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout.strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--image", action="append", default=[], help="image reference")
    parser.add_argument("--app", action="append", default=[], help="Container App to read")
    parser.add_argument("--resource-group", default="ama")
    parser.add_argument("--ref", default="HEAD")
    parser.add_argument("--dockerfile", default="src/api/Dockerfile")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    images = list(args.image)
    images += [image_from_azure(args.resource_group, app) for app in args.app]
    if not images:
        parser.error("give at least one --image or --app")
    statuses = []
    for image in images:
        status, detail = check_image(args.root, image, args.ref, args.dockerfile)
        statuses.append(status)
        print(f"{status}: {image}: {detail}")
    if "failed" in statuses:
        return 1
    return 2 if "unverifiable" in statuses else 0


if __name__ == "__main__":
    sys.exit(main())
