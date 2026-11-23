#!/usr/bin/env python3
"""Keep native tmux RPI workers running: launch the next eligible issue when a slot is free.

Run it in its own tmux session from any checkout:

    tmux new-session -d -s refill "python3 tools/coordinator/refill.py"

Settings live in tools/coordinator/config.json (priority and skip sets, launch limit). The
worker cap is read from the file named by AMA_REFILL_MAX (default /tmp/refill.max); create
a /tmp/refill.stop file to stop the loop. /tmp does not survive a VM restart, so the
cap defaults to config.json "default_cap" when the file is missing.
"""

import datetime
import json
import os
import re
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CONFIG = json.load(open(os.path.join(HERE, "config.json")))
STATE = os.path.expanduser(os.environ.get("AMA_COORD_STATE", "~/.local/share/ama/coord"))
LOG = os.environ.get("AMA_REFILL_LOG", "/tmp/refill.log")
CAP_FILE = os.environ.get("AMA_REFILL_MAX", "/tmp/refill.max")
STOP_FILE = "/tmp/refill.stop"
SKIP = set(CONFIG["skip"])
PRIORITY = set(CONFIG["priority"])
COOLDOWN_HOURS = CONFIG.get("relaunch_cooldown_hours", 3)
PROJECT_ID = CONFIG["project_id"]
STATUS_FIELD = CONFIG["status_field_id"]
IN_PROGRESS_OPTION = CONFIG["in_progress_option_id"]
MIN_FREE_GB = CONFIG["min_free_gb"]
PROJECT_OWNER = CONFIG["project_owner"]
PROJECT_NUMBER = CONFIG["project_number"]
WITNESS = os.path.expanduser("~/.local/share/ama/phase-witness")


def sh(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=REPO).stdout


def log(msg: str) -> None:
    with open(LOG, "a") as f:
        f.write(f"{datetime.datetime.now(datetime.UTC):%Y-%m-%dT%H:%M:%SZ} {msg}\n")


def live() -> set[int]:
    return {int(m) for m in re.findall(r"rpi-(\d+)-live", sh("tmux ls 2>/dev/null"))}


def issue_times() -> dict[int, str]:
    d: dict[int, str] = {}
    for f in os.listdir("/tmp"):
        m = re.match(r"brief-(\d+)-live-(\d{8}T\d{6}Z)\.md$", f)
        if m:
            d[int(m.group(1))] = max(d.get(int(m.group(1)), ""), m.group(2))
    if os.path.isdir(WITNESS):
        for name in os.listdir(WITNESS):
            m = re.match(r"(\d+)-live-(\d{8}T\d{4,6}Z?)$", name)
            if m:
                d[int(m.group(1))] = max(d.get(int(m.group(1)), ""), m.group(2))
    return d


def board() -> list[tuple[int, str]]:
    out = sh(
        f"gh project item-list {PROJECT_NUMBER} --owner {PROJECT_OWNER} --limit 400 --format json"
    )
    cache = os.path.join(STATE, "board-cache.json")
    try:
        items = json.loads(out)["items"]
        os.makedirs(STATE, exist_ok=True)
        open(cache, "w").write(out)
    except Exception:
        try:
            items = json.load(open(cache))["items"]
        except Exception:
            return []
    res = []
    for i in items:
        c = i.get("content") or {}
        if i.get("status") in ("Todo", "In Progress") and c.get("number"):
            res.append((c["number"], c.get("title", "")))
    return res


def launch_counts() -> dict[int, int]:
    counts: dict[int, int] = {}
    for f in os.listdir("/tmp"):
        m = re.match(r"brief-(\d+)-live-", f)
        if m:
            counts[int(m.group(1))] = counts.get(int(m.group(1)), 0) + 1
    return counts


def cooled_down(n: int, times: dict[int, str]) -> bool:
    """An issue relaunches once its last worker is older than the cooldown (epics wait longer)."""
    last = times.get(n)
    if not last:
        return True
    try:
        t = datetime.datetime.strptime(last[:15], "%Y%m%dT%H%M%S").replace(tzinfo=datetime.UTC)
    except ValueError:
        return True
    return (datetime.datetime.now(datetime.UTC) - t).total_seconds() > COOLDOWN_HOURS * 3600


def mark_in_progress(n: int) -> None:
    try:
        items = json.load(open(os.path.join(STATE, "board-cache.json")))["items"]
        item = next(i for i in items if (i.get("content") or {}).get("number") == n)
        sh(
            f"gh project item-edit --project-id {PROJECT_ID} --id {item['id']} "
            f"--field-id {STATUS_FIELD} --single-select-option-id {IN_PROGRESS_OPTION}"
        )
    except Exception:
        log(f"board status not updated for {n}")


def candidates(lv: set[int]) -> list[tuple[int, str, int, str]]:
    times = issue_times()
    bl = board()
    try:
        op = json.loads(
            sh(
                "gh api 'repos/jmservera/ama/issues?state=open&per_page=100' "
                "--jq '[.[]|select(.pull_request==null)|{n:.number,t:.title}]'"
            )
        )
        have = {n for n, _ in bl}
        bl += [(o["n"], o["t"]) for o in op if o["n"] in PRIORITY and o["n"] not in have]
    except Exception:
        pass
    cands = [
        (0 if n in PRIORITY else 1, times.get(n, ""), n, t)
        for n, t in bl
        if n not in lv and n not in SKIP and cooled_down(n, times)
    ]
    cands = [(0 if "Epic" not in t else 2, a, n, t) for _, a, n, t in cands]
    cands.sort()
    return cands


def main() -> None:
    while True:
        if os.path.exists(STOP_FILE):
            log("stop file present; exiting (the wrapper stops too)")
            break
        try:
            cap = int(open(CAP_FILE).read().strip())
        except Exception:
            cap = CONFIG["default_cap"]
        lv = live()
        st = os.statvfs("/")
        if st.f_bavail * st.f_frsize < MIN_FREE_GB * 2**30:
            log(f"low disk (<{MIN_FREE_GB} GB free): launch paused")
            time.sleep(60)
            continue
        if len(lv) < cap:
            cands = candidates(lv)
            if cands:
                _, _, n, title = cands[0]
                goal = (
                    f"Issue title: {title}. Close the issue's remaining acceptance criteria for "
                    "the demo: prove every criterion that can be proven with recorded evidence, "
                    "implement and test any real defect you find (src changes use the full tier "
                    "and stay a local commit), and record exactly what is unproven and why."
                )
                log(f"launch {n} (live={len(lv)} max={cap})")
                out = sh(f"bash {HERE}/mk-live.sh {n} code {json.dumps(goal)} 2>&1 | tail -3")
                log(out.strip().replace("\n", " | ")[:300])
                mark_in_progress(n)
                time.sleep(20)
                continue
            log("no candidates")
        time.sleep(60)


if __name__ == "__main__":
    main()
