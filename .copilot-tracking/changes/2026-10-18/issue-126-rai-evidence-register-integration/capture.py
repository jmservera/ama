"""Capture exact task-owned Git integration evidence without changing source."""

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

OLD_BASE = "ab0613f3336109ff9b96560a16758ee842232715"
OLD_HEAD = "4a23f750f1ea943bb4aaf989256e7bd019a57d12"
TARGET = "9403dc6a8f52f1f04c5ad910faab11a57c29ee78"
SESSION = Path("/home/azureuser/.copilot/session-state/10f40604-edc8-40bb-9368-73353faf82a1/files")
ROOT = SESSION / "issue126-integration-evidence"
ROOT.mkdir(exist_ok=True)


def git(*args):
    return subprocess.check_output(["git", *args])


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def tree(ref):
    rows = []
    for raw in git("ls-tree", "-r", "-z", ref).split(b"\0"):
        if raw:
            meta, path = raw.split(b"\t", 1)
            mode, kind, oid = meta.decode().split()
            rows.append((path.decode(), mode, kind, oid))
    output = subprocess.check_output(
        ["git", "cat-file", "--batch"],
        input=b"".join(oid.encode() + b"\n" for _, _, _, oid in rows),
    )
    cursor = 0
    result = {}
    for path, mode, kind, oid in rows:
        end = output.index(b"\n", cursor)
        returned, returned_kind, size = output[cursor:end].decode().split()
        assert returned == oid and returned_kind == kind
        size = int(size)
        cursor = end + 1
        data = output[cursor:cursor + size]
        cursor += size + 1
        result[path] = dict(mode=mode, oid=oid, sha256=digest(data), bytes=size)
    return result


def paths(base, head):
    return git("diff", "--name-only", base, head).decode().splitlines()


def normalized(base, head, selected):
    patch = git(
        "diff", "--no-ext-diff", "--no-color", "--no-renames", "--full-index",
        "--unified=0", base, head, "--", *selected,
    ).decode()
    patch = re.sub(r"^index .*\n", "", patch, flags=re.MULTILINE)
    return re.sub(r"^@@.*\n", "@@\n", patch, flags=re.MULTILINE).encode()


scope = paths(OLD_BASE, OLD_HEAD)
assert len(scope) == 30
stage = sys.argv[1]
if stage == "before":
    assert git("status", "--porcelain") == b""
    assert git("rev-parse", "HEAD").decode().strip() == OLD_HEAD
    write("before-full-tree.json", tree(OLD_HEAD))
    write("target-full-tree.json", tree(TARGET))
    write("old-base-full-tree.json", tree(OLD_BASE))
    (ROOT / "original-30-paths.txt").write_text("\n".join(scope) + "\n")
    for name, selected in (
        ("owned-all", scope),
        ("owned-source", [p for p in scope if p.startswith("src/") and not p.endswith("README.md")]),
    ):
        patch = normalized(OLD_BASE, OLD_HEAD, selected)
        (ROOT / f"{name}-before.normalized.patch").write_bytes(patch)
    write("integration-intent.json", dict(
        task_id="126", task_slug="issue-126-rai-evidence-register",
        operation="integration-only rebase-onto", old_base=OLD_BASE, old_head=OLD_HEAD,
        exact_target=TARGET, authorized_remote_lease=OLD_HEAD,
        phase="Follow-up", next_action="Rebase owned two commits; additive conflicts only",
        original_execution_log=dict(
            source="/tmp/rpi-126-register.log",
            session_copy=str(SESSION / "issue126-original-complete-execution.log"),
            sha256=digest((SESSION / "issue126-original-complete-execution.log").read_bytes()),
            bytes=(SESSION / "issue126-original-complete-execution.log").stat().st_size,
            complete_read=True,
        ),
    ))
    print("Before: full old-base/topic/target trees, exact original30 and normalized patches captured")
elif stage == "after":
    head = git("rev-parse", "HEAD").decode().strip()
    current = tree(head)
    old = json.loads((ROOT / "before-full-tree.json").read_text())
    target = json.loads((ROOT / "target-full-tree.json").read_text())
    write("rebased-full-tree.json", current)
    assert set(paths(TARGET, head)) == set(scope), "Owned 30-path scope changed"
    unchanged_upstream = [p for p in target if p not in scope]
    assert all(current.get(p) == target[p] for p in unchanged_upstream), "Protected upstream changed"
    protected = {
        p: target[p] for p in paths(OLD_BASE, TARGET) if p not in scope
    }
    write("protected-upstream-path-hashes.json", protected)
    immutable = [
        p for p in scope if p.startswith(".copilot-tracking/")
    ] + [
        "docs/case_study_48_original.md", "docs/reference/memory.md",
        ".copilot-tracking/rai-reviews/2026-10-14/rai-report-ama-20261014.md",
    ]
    assert all(current[p] == old[p] for p in immutable), "Original evidence bytes/mode changed"
    write("immutable-original-path-hashes.json", {p: current[p] for p in immutable})
    parity = {}
    for name, selected in (
        ("owned-all", scope),
        ("owned-source", [p for p in scope if p.startswith("src/") and not p.endswith("README.md")]),
    ):
        patch = normalized(TARGET, head, selected)
        (ROOT / f"{name}-after.normalized.patch").write_bytes(patch)
        before = (ROOT / f"{name}-before.normalized.patch").read_bytes()
        parity[name] = dict(
            identical=before == patch,
            before_sha256=digest(before), after_sha256=digest(patch),
            normalization="git diff U0; remove index object IDs and hunk positions only; retain exact change-line bytes",
            paths=selected,
        )
    assert parity["owned-source"]["identical"], "Owned source patch changed"
    target_log = git("show", TARGET + ":docs/reference/log.md")
    merged_log = git("show", head + ":docs/reference/log.md")
    assert merged_log.startswith(target_log), "Upstream append-only log is not intact prefix"
    original_log = git("show", OLD_HEAD + ":docs/reference/log.md")
    base_log = git("show", OLD_BASE + ":docs/reference/log.md")
    assert original_log.startswith(base_log)
    assert merged_log == target_log + original_log[len(base_log):], "Original log addition changed"
    before_server = git("show", OLD_HEAD + ":src/api/src/zava_forward/api/server.py")
    server = git("show", head + ":src/api/src/zava_forward/api/server.py")
    original_server = git("show", OLD_BASE + ":src/api/src/zava_forward/api/server.py")
    target_server = git("show", TARGET + ":src/api/src/zava_forward/api/server.py")
    upstream_addition = target_server.replace(original_server, b"") if original_server in target_server else None
    consultation = b'            elif kind == "packages" and len(rest) == 2 and rest[1] == "consultation":\n                s.record_consultation(u, rest[0], body)\n'
    assert server.count(consultation) == 1 and target_server.count(consultation) == 1
    assert server.replace(consultation, b"") == before_server, "Server not exact additive union"
    parity.update(dict(
        rebased_head=head, target=TARGET, original_head=OLD_HEAD,
        original_scope_count=len(scope), all_nonowned_target_paths_preserved=len(unchanged_upstream),
        protected_upstream_paths=sorted(protected), immutable_originals_preserved=len(immutable),
        log_exact_additive_union=True, server_exact_additive_union=True,
        no_source_corrections=True, critique_executions_added=0, review_executions_added=0,
    ))
    write("parity.json", parity)
    print(json.dumps(parity, indent=2))
else:
    raise SystemExit("Use before or after")
