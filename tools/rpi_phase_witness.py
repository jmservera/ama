"""Local observational witness for RPI phase boundaries (issue #1300).

It records what it observes at the moment it is invoked: its own UTC clock,
event order, Git HEAD/tree, scoped dirty-state identities and the canonical RPI
artifacts named by the session state. It does not replace the RPI state or
gates. The log is a locally writable hash-chained JSONL file: it is not
tamperproof, not host or model attestation and not proof of unobserved
reasoning. Actor, session and model values are caller assertions.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

EVENTS = (
    "launch",
    "research-open",
    "plan-done",
    "implement-start",
    "implement-done",
    "review-done",
    "commit-complete",
)
ORDER = {name: index for index, name in enumerate(EVENTS)}
REQUIRED = {
    "research-open": ("research",),
    "plan-done": ("plan", "details", "critique"),
    "implement-start": ("changes",),
    "implement-done": ("changes",),
    "review-done": ("review",),
    "commit-complete": ("review", "changes"),
}
ARTIFACT_KEYS = ("research", "plan", "details", "critique", "changes", "review")
# Revisions to these after observation weaken the claim; the others legitimately evolve.
GUARDED = ("critique", "review")
TRACKING = ".copilot-tracking"
LIMITS = (
    "Local writable record: not tamperproof, not host or model attestation, "
    "not proof of unobserved reasoning; asserted labels are not observed."
)


class Refusal(Exception):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        raise Refusal(f"git {args[0]} failed")
    return result.stdout if result.returncode == 0 else ""


def record_hash(record: dict) -> str:
    body = {key: value for key, value in record.items() if key != "record_hash"}
    blob = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()


def log_paths(
    repo: Path, issue: str, evidence_dir: Path | None = None
) -> tuple[Path, Path]:
    if evidence_dir is not None:
        directory = evidence_dir / f"issue-{issue}"
    else:
        directory = repo / TRACKING / "phase-witness" / f"issue-{issue}"
    return directory / "events.jsonl", directory / "events.lock"


def read_log(path: Path, data: bytes | None = None) -> tuple[list[dict], list[str]]:
    """Return valid records and structural problems (torn lines, chain breaks)."""
    records: list[dict] = []
    problems: list[str] = []
    if data is None:
        if not path.exists():
            return records, problems
        data = path.read_bytes()
    previous = ""
    for number, raw in enumerate(data.split(b"\n"), start=1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
            if not isinstance(record, dict) or "record_hash" not in record:
                raise ValueError
        except ValueError:
            problems.append(f"line {number}: unreadable or torn record kept as found")
            continue
        if record["record_hash"] != record_hash(record):
            problems.append(f"line {number}: record hash mismatch")
        elif record.get("prev_hash") != previous:
            problems.append(f"line {number}: chain break")
        previous = record["record_hash"]
        records.append(record)
    return records, problems


def dirty_identities(repo: Path) -> tuple[dict, dict]:
    """Return (source, artifacts) maps of dirty path -> sha256 or 'deleted'."""
    out = git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    source: dict[str, str] = {}
    artifacts: dict[str, str] = {}
    items = out.split("\0")
    index = 0
    while index < len(items):
        entry = items[index]
        index += 1
        if len(entry) < 4:
            continue
        status, rel = entry[:2], entry[3:]
        if "R" in status or "C" in status:
            index += 1  # skip the origin path of a rename or copy
        path = repo / rel
        is_artifact = rel.startswith(TRACKING + "/")
        if is_artifact and not inside_tracking(repo, path):
            identity = "outside-tracking-not-read"
        elif path.is_file() and not path.is_symlink():
            identity = sha256_file(path)
        else:
            identity = "deleted"
        target = artifacts if is_artifact else source
        target[rel] = identity
    return dict(sorted(source.items())), dict(sorted(artifacts.items()))


def inside_tracking(repo: Path, candidate: Path) -> bool:
    """True only if the tracking root stays under the repo and the target under the root.

    Resolution follows symlinks but never opens or reads the target.
    """
    try:
        tracking = (repo / TRACKING).resolve()
        tracking.relative_to(repo.resolve())
        candidate.resolve().relative_to(tracking)
    except ValueError:
        return False
    return True


def log_contained(
    repo: Path, issue: str, evidence_dir: Path | None = None
) -> str | None:
    """Return None when the log and lock are acceptable, else the refusal reason."""
    path, lock_path = log_paths(repo, issue, evidence_dir)
    if evidence_dir is None:
        ok = all(inside_tracking(repo, item) for item in (path.parent, path, lock_path))
        return None if ok else "witness log path escapes the repository tracking root"
    if not evidence_dir.is_absolute():
        return "evidence directory must be an absolute path"
    top = git(repo, "rev-parse", "--show-toplevel", check=False).strip()
    if not top or Path(top).resolve() != repo.resolve():
        return "--repo must be the Git worktree root when using an evidence directory"
    root = evidence_dir.resolve()
    if root == repo.resolve() or repo.resolve() in root.parents:
        return "evidence directory must be outside the candidate worktree"
    try:
        for item in (path.parent, path, lock_path):
            item.resolve().relative_to(root)
    except ValueError:
        return "witness log path escapes the evidence directory"
    top_resolved = repo.resolve()
    for item in (path.parent, path, lock_path):
        resolved = item.resolve()
        if resolved == top_resolved or top_resolved in resolved.parents:
            return (
                "derived witness log destination must be outside the candidate worktree"
            )
    return None


def early_source_changes(repo: Path, records: list[dict], head: str) -> list[str]:
    """Qualify committed source changes between the earliest observed HEAD and now."""
    first = next((r["git"]["head"] for r in records if r["outcome"] == "ok"), None)
    if not first or first == head:
        return []
    ancestor = subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", first, head],
        capture_output=True,
        check=False,
    )
    diff = subprocess.run(
        ["git", "-C", str(repo), "diff", "--name-only", "-z", first, head],
        capture_output=True,
        check=False,
    )
    if ancestor.returncode != 0 or diff.returncode != 0:
        return ["unable to compare the earliest observed HEAD with the opening HEAD"]
    changed = [
        p
        for p in diff.stdout.decode(errors="replace").split("\0")
        if p and not p.startswith(TRACKING + "/")
    ]
    if not changed:
        return []
    return [
        "source changed in committed history before implement-start: "
        + ", ".join(changed)
    ]


def load_artifacts(repo: Path, state_path: Path | None, event: str) -> dict:
    if event == "launch":
        return {}
    if state_path is None:
        raise Refusal("a canonical state file is required for this event")
    if not inside_tracking(repo, state_path) or not state_path.is_file():
        raise Refusal("state file must be a regular file inside .copilot-tracking")
    try:
        state = json.loads(state_path.read_text())
        listed = state["artifact_paths"]
    except (ValueError, KeyError, TypeError):
        raise Refusal("state file is not canonical RPI state JSON") from None
    found: dict[str, dict] = {}
    for key in ARTIFACT_KEYS:
        rel = listed.get(key) if isinstance(listed, dict) else None
        if not isinstance(rel, str) or os.path.isabs(rel):
            continue
        path = repo / rel
        if (
            not inside_tracking(repo, path)
            or not path.is_file()
            or path.stat().st_size == 0
        ):
            continue
        info = path.stat()
        found[key] = {
            "path": rel,
            "sha256": sha256_file(path),
            "size": info.st_size,
            "mtime_ns": info.st_mtime_ns,
        }
    missing = [key for key in REQUIRED[event] if key not in found]
    if missing:
        raise Refusal("missing persisted artifact evidence: " + ", ".join(missing))
    found["state"] = {
        "path": str(state_path.resolve().relative_to(repo.resolve())),
        "sha256": sha256_file(state_path),
    }
    return found


def last_ok(records: list[dict], event: str) -> dict | None:
    for record in reversed(records):
        if record["event"] == event and record["outcome"] == "ok":
            return record
    return None


def check_commit_claim(
    repo: Path, claim: str | None, records: list[dict], source: dict
) -> None:
    head = git(repo, "rev-parse", "HEAD").strip()
    start = last_ok(records, "implement-start")
    review = last_ok(records, "review-done")
    if not claim or claim != head:
        raise Refusal("commit claim does not match the actual HEAD")
    if start is None or review is None:
        raise Refusal(
            "no observed implement-start and review-done to bind the commit to"
        )
    if (
        head == start["git"]["head"]
        or subprocess.run(
            [
                "git",
                "-C",
                str(repo),
                "merge-base",
                "--is-ancestor",
                start["git"]["head"],
                head,
            ],
            capture_output=True,
            check=False,
        ).returncode
        != 0
    ):
        raise Refusal("no new commit descending from the implement-start HEAD exists")
    if source:
        raise Refusal("source is still dirty; the claimed commit does not hold it")
    reviewed = review["git"]["dirty_source"]
    for rel, identity in reviewed.items():
        in_head = subprocess.run(
            ["git", "-C", str(repo), "show", f"HEAD:{rel}"],
            capture_output=True,
            check=False,
        )
        actual = (
            hashlib.sha256(in_head.stdout).hexdigest()
            if in_head.returncode == 0
            else "deleted"
        )
        if actual != identity:
            raise Refusal(f"commit content differs from the reviewed source for {rel}")
    changed = git(
        repo, "diff", "--name-only", review["git"]["head"], "HEAD"
    ).splitlines()
    extra = [
        p for p in changed if not p.startswith(TRACKING + "/") and p not in reviewed
    ]
    if extra:
        raise Refusal(
            "commit changes source that was not part of the reviewed snapshot: "
            + ", ".join(extra)
        )


class Mismatch(Exception):
    pass


def bound_elsewhere(
    records: list[dict], repo: Path, issue: str, external: bool
) -> bool:
    """An in-tree log is bound by its path; only an external log needs the check."""
    return external and any(
        r.get("worktree") != str(repo) or r.get("issue") != issue for r in records
    )


def append(path: Path, lock_path: Path, build) -> tuple[dict, bool]:
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_fd = os.open(lock_path, os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW, 0o644)
    with os.fdopen(lock_fd, "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        records, _ = read_log(path)
        record = build(records)
        data = (
            json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode()
        fd = os.open(path, os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW, 0o644)
        try:
            size = os.fstat(fd).st_size
            if size and os.pread(fd, 1, size - 1) != b"\n":
                data = b"\n" + data
            os.write(fd, data)
            os.fsync(fd)
        finally:
            os.close(fd)
    return record, record["outcome"] == "ok"


def record_event(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    state_path = Path(args.state) if args.state else None
    if state_path is not None and not state_path.is_absolute():
        state_path = repo / state_path
    evidence_dir = Path(args.evidence_dir) if args.evidence_dir else None
    path, lock_path = log_paths(repo, args.issue, evidence_dir)
    reason = log_contained(repo, args.issue, evidence_dir)
    if reason:
        print(json.dumps({"outcome": "refused", "reasons": [reason]}))
        return 2

    def build(records: list[dict]) -> dict:
        if bound_elsewhere(records, repo, args.issue, evidence_dir is not None):
            raise Mismatch
        now = datetime.now(UTC)
        reasons: list[str] = []
        qualifications: list[str] = []
        artifacts: dict = {}
        brief = None
        git_info: dict = {}
        try:
            head = git(repo, "rev-parse", "HEAD").strip()
            tree = git(repo, "rev-parse", "HEAD^{tree}").strip()
            source, artifact_dirty = dirty_identities(repo)
            git_info = {
                "head": head,
                "tree": tree,
                "dirty_source": source,
                "dirty_artifacts": artifact_dirty,
            }
            if args.event == "launch":
                brief_path = Path(args.brief) if args.brief else None
                if brief_path is None or not brief_path.is_file():
                    raise Refusal("launch requires an existing brief file")
                brief = {
                    "path": str(brief_path.resolve()),
                    "sha256": sha256_file(brief_path),
                }
            else:
                artifacts = load_artifacts(repo, state_path, args.event)
            if args.event == "commit-complete":
                check_commit_claim(repo, args.claim_commit, records, source)
            seen = [r["event"] for r in records if r["outcome"] == "ok"]
            order = ORDER[args.event]
            if order > 0:
                missing = [e for e in EVENTS[:order] if e not in seen]
                if missing:
                    qualifications.append(
                        "missing observed predecessor: " + ", ".join(missing)
                    )
            if any(ORDER[e] > order for e in seen):
                qualifications.append("recorded after a later boundary")
            if args.event == "implement-start":
                if source:
                    qualifications.append(
                        "source was already dirty at implement-start; edits predate this witness"
                    )
                qualifications.extend(early_source_changes(repo, records, head))
            if records and now < datetime.fromisoformat(records[-1]["utc"]):
                qualifications.append("clock earlier than the previous record")
        except Refusal as error:
            reasons.append(str(error))
        previous = records[-1]["record_hash"] if records else ""
        record = {
            "seq": (records[-1]["seq"] + 1) if records else 1,
            "prev_hash": previous,
            "event": args.event,
            "outcome": "refused" if reasons else "ok",
            "reasons": reasons,
            "qualifications": qualifications,
            "utc": now.isoformat(timespec="microseconds"),
            "monotonic_ns": time.monotonic_ns(),
            "observer_pid": os.getpid(),
            "issue": args.issue,
            "worktree": str(repo),
            "git": git_info,
            "brief": brief,
            "artifacts": artifacts,
            "asserted": {
                "actor": args.actor,
                "session": args.session,
                "model": args.claim_model,
                "commit_claim": args.claim_commit,
            },
            "limits": LIMITS,
        }
        record["record_hash"] = record_hash(record)
        return record

    try:
        record, ok = append(path, lock_path, build)
    except Mismatch:
        print(
            json.dumps(
                {
                    "outcome": "refused",
                    "reasons": [
                        "evidence log is bound to a different worktree or issue"
                    ],
                }
            )
        )
        return 2
    print(
        json.dumps(
            {
                "seq": record["seq"],
                "event": record["event"],
                "outcome": record["outcome"],
                "utc": record["utc"],
                "reasons": record["reasons"],
                "qualifications": record["qualifications"],
            }
        )
    )
    return 0 if ok else 2


def verify(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    evidence_dir = Path(args.evidence_dir) if args.evidence_dir else None
    path, _ = log_paths(repo, args.issue, evidence_dir)
    notes: list[str] = []
    reason = log_contained(repo, args.issue, evidence_dir)
    log_sha = None
    if reason is None:
        data = path.read_bytes() if path.is_file() else b""
        log_sha = hashlib.sha256(data).hexdigest() if data else None
        records, problems = read_log(path, data)
        findings: list[str] = list(problems)
        if not records:
            findings.append("no witness records found")
        findings.extend(
            f"seq {r.get('seq')} {r.get('event')}: record is bound to a different worktree or issue"
            for r in records
            if bound_elsewhere([r], repo, args.issue, evidence_dir is not None)
        )
    else:
        records = []
        findings = [f"{reason}; not read"]
    seen: list[str] = []
    previous_utc = None
    for record in records:
        label = f"seq {record['seq']} {record['event']}"
        if record["outcome"] == "refused":
            findings.append(f"{label}: refused: {'; '.join(record['reasons'])}")
            continue
        findings.extend(f"{label}: {q}" for q in record["qualifications"])
        utc = datetime.fromisoformat(record["utc"])
        if previous_utc and utc < previous_utc:
            findings.append(f"{label}: clock earlier than the previous record")
        previous_utc = utc
        seen.append(record["event"])
    for event in EVENTS:
        if event not in seen:
            findings.append(f"no successful observation of {event}")
    for record in records:
        if record["outcome"] != "ok":
            continue
        for key, info in record["artifacts"].items():
            current = repo / info["path"]
            if not inside_tracking(repo, current):
                findings.append(
                    f"seq {record['seq']} {record['event']}: {key} artifact path "
                    "escapes the tracking root; not read"
                )
                continue
            if not current.is_file() or sha256_file(current) != info["sha256"]:
                target = findings if key in GUARDED else notes
                target.append(
                    f"seq {record['seq']} {record['event']}: {key} artifact changed after observation"
                )
    review = last_ok(records, "review-done")
    if review:
        source, _ = dirty_identities(repo)
        reviewed = review["git"]["dirty_source"]
        commit = last_ok(records, "commit-complete")
        baseline = (
            commit["git"]["head"] if commit and not source else review["git"]["head"]
        )
        allowed = set(reviewed) if baseline == review["git"]["head"] else set()
        changed = git(
            repo, "diff", "--name-only", baseline, "HEAD", check=False
        ).splitlines()
        stale = any(
            not p.startswith(TRACKING + "/") and p not in allowed for p in changed
        )
        if commit and not source:
            pass
        elif source != reviewed:
            stale = True
        if stale:
            findings.append(
                "review source is stale: the current source differs from the reviewed source"
            )
    final = {
        "head": git(repo, "rev-parse", "HEAD", check=False).strip(),
        "tree": git(repo, "rev-parse", "HEAD^{tree}", check=False).strip(),
        "log_sha256": log_sha,
    }
    done = last_ok(records, "commit-complete")
    if done and done["git"]["head"] != final["head"]:
        findings.append("HEAD differs from the head claimed at commit-complete")
    report = {
        "issue": args.issue,
        "final": final,
        "records": len(records),
        "findings": findings,
        "notes": notes,
        "limits": LIMITS,
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"records: {len(records)}")
        print(f"final: head {final['head']} tree {final['tree']} log {log_sha}")
        for line in findings:
            print("QUALIFIED: " + line)
        for line in notes:
            print("note: " + line)
        print(LIMITS)
    return 1 if findings else 0


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        sys.stderr.write(f"error: {message}\n")
        raise SystemExit(64)


def main(argv: list[str] | None = None) -> int:
    parser = Parser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    rec = sub.add_parser("record", help="observe and append one boundary")
    rec.add_argument("event", choices=EVENTS)
    ver = sub.add_parser("verify", help="re-read the log against the current tree")
    ver.add_argument("--json", action="store_true")
    for item in (rec, ver):
        item.add_argument("--repo", required=True)
        item.add_argument("--issue", required=True)
        item.add_argument("--evidence-dir")
    rec.add_argument("--state")
    rec.add_argument("--brief")
    rec.add_argument("--session")
    rec.add_argument("--actor", choices=("coordinator", "worker"), default="worker")
    rec.add_argument("--claim-model")
    rec.add_argument("--claim-commit")
    args = parser.parse_args(argv)
    if not args.issue.isdigit():
        parser.error("--issue must be the issue number")
    return record_event(args) if args.command == "record" else verify(args)


if __name__ == "__main__":
    raise SystemExit(main())
