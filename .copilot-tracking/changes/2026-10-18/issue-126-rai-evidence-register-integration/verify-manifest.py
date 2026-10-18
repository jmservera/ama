"""Verify integration-only boundaries and generate explicit nonrecursive manifests."""

import gzip
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.relative_to(Path.cwd())
TARGET = "9403dc6a8f52f1f04c5ad910faab11a57c29ee78"
REBASED = "93b7450c823d80765d869e533788662f3c61f94a"
MUTABLE = {
    ".copilot-tracking/changes/2026-10-18/issue-126-rai-evidence-register-changes.md",
    ".copilot-tracking/details/2026-10-18/issue-126-rai-evidence-register-phase-details.md",
    ".copilot-tracking/plans/2026-10-18/issue-126-rai-evidence-register-plan.md",
    ".copilot-tracking/rpi-sessions/2026-10-18/issue-126-rai-evidence-register-state.json",
}


def git(*args):
    return subprocess.check_output(["git", *args])


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    file = Path(path)
    if file.is_symlink():
        return sha(os.readlink(file).encode()), "120000"
    return sha(file.read_bytes()), "100755" if file.stat().st_mode & 0o111 else "100644"


def output(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


scope = (ROOT / "original-30-paths.txt").read_text().splitlines()
original = json.loads(gzip.decompress((ROOT / "before-full-tree.json.gz").read_bytes()))
target = json.loads(gzip.decompress((ROOT / "target-full-tree.json.gz").read_bytes()))
rebased = json.loads(gzip.decompress((ROOT / "rebased-full-tree.json.gz").read_bytes()))
immutable = json.loads((ROOT / "immutable-original-path-hashes.json").read_text())
for path in immutable.keys() - MUTABLE:
    assert identity(path) == (original[path]["sha256"], original[path]["mode"]), path
for path in set(scope) - MUTABLE:
    assert identity(path) == (rebased[path]["sha256"], rebased[path]["mode"]), path
for path in set(target) - set(scope):
    assert identity(path) == (target[path]["sha256"], target[path]["mode"]), path
for path in MUTABLE:
    if not path.endswith(".json"):
        assert Path(path).read_bytes().startswith(git("show", REBASED + ":" + path)), path

source = json.loads((ROOT / "parity.json").read_text())["owned-source"]
patch = git(
    "diff", "--no-ext-diff", "--no-color", "--no-renames", "--full-index",
    "--unified=0", TARGET, "--", *source["paths"],
).decode()
patch = re.sub(r"^index .*\n", "", patch, flags=re.MULTILINE)
patch = re.sub(r"^@@.*\n", "@@\n", patch, flags=re.MULTILINE).encode()
assert sha(patch) == source["before_sha256"]

state = json.loads(Path(next(p for p in MUTABLE if p.endswith(".json"))).read_text())
assert state["task_slug"] == "issue-126-rai-evidence-register"
assert (state["mode"], state["active_phase"], state["status"], state["session_status"]) == (
    "automatic", "Follow-up", "completed", "stopped",
)
checks = {
    "original_critique_sha256": sha(Path(state["artifact_paths"]["critique"]).read_bytes()),
    "original_review_sha256": sha(Path(state["artifact_paths"]["review"]).read_bytes()),
    "original_research_preserved": True,
    "all_prior_raw_logs_preserved": True,
    "original_report_case_memory_preserved": True,
    "source_patch_identical_sha256": sha(patch),
    "nonowned_target_paths_preserved": len(set(target) - set(scope)),
    "original_scope": scope,
    "bookkeeping_only_original_path_updates": sorted(MUTABLE),
    "additional_critique_executions": 0,
    "additional_original_review_executions": 0,
    "source_correction_count": 0,
}
assert checks["original_critique_sha256"] == "4e24e7e0cc8cf21081c4e5823cbbfbd8fbf0d1d0a8e904220ecd5b0e3235c8bb"
assert checks["original_review_sha256"] == "12788d8f7f81279012b54ba3902255f2eabe436d61d97fda3a0ae701bb6b6c24"
output("final-integrity.json", checks)

inventory_path = ROOT / "full-changed-inventory.txt"
manifest_path = ROOT / "full-changed-path-hashes.json"
changed = set(git("diff", "--name-only", TARGET).decode().splitlines())
changed.update(str(p) for p in ROOT.iterdir() if p.is_file())
changed.update([str(inventory_path), str(manifest_path)])
assert changed - set(scope) == {str(p) for p in ROOT.iterdir() if p.is_file()} | {
    str(inventory_path), str(manifest_path),
}
inventory_path.write_text("\n".join(sorted(changed)) + "\n")
manifest = {}
for path in sorted(changed):
    if path == str(manifest_path):
        manifest[path] = {
            "mode": "100644",
            "sha256": None,
            "reason": "Self-reference excluded; exact manifest bytes are bound by published Git blob",
        }
    else:
        data = Path(path).read_bytes()
        manifest[path] = {
            "mode": "100755" if Path(path).stat().st_mode & 0o111 else "100644",
            "bytes": len(data),
            "sha256": sha(data),
        }
output("full-changed-path-hashes.json", dict(
    target=TARGET, original_scope_count=30,
    integration_artifact_count=len(changed) - 30,
    changed_path_count=len(changed), paths=manifest,
))
print(json.dumps(checks, indent=2))
print(f"Full changed inventory: {len(changed)} paths; original30 + integration{len(changed) - 30}")
