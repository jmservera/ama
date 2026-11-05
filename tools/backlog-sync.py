#!/usr/bin/env python3
"""Audit and repair the GitHub backlog against the project board.

Default is a read-only audit. Use --apply to write. Rules:

* Closed issue: board Done and every acceptance checkbox ticked.
* Open issue on the board as Done: back to Todo (criteria are unmet).
* Open issue named by --active (coordinator-confirmed live session or frozen
  unpublished candidate): In Progress, even with merged PRs and no open PR.
* Open issue In Progress with no open PR: Todo only when named by --inactive
  (expressly confirmed to have no session and no frozen candidate). Otherwise
  activity is Unknown: the status is kept and reported as unverified.
  --active is positive evidence only; omission from it never demotes.
* Open issue Todo with an open PR that references it: In Progress.
* Issue missing from the board: added with the status implied above.

Open issues with merged PR references but unticked criteria are listed for
human or coordinator review because criteria need evidence to be ticked.
A worktree, a missing upstream or an unknown session is not activity or proof
of completion. Use --active 79,80 and --inactive 90; unknown or closed issue
numbers, overlap between the two, or a malformed list stop the run before any write.
Requires the gh CLI with the project scope.
"""

import argparse
import json
import re
import subprocess

REPO = "jmservera/ama"
OWNER = "jmservera"
PROJECT = 7
UNTICKED = re.compile(r"^(\s*[-*] )\[ \]", re.M)


def gh(*args, data=None):
    out = subprocess.run(["gh", *args], capture_output=True, text=True, input=data)
    if out.returncode:
        raise SystemExit(f"gh {' '.join(args[:3])} failed: {out.stderr.strip()}")
    return out.stdout


def gh_json(*args):
    return json.loads(gh(*args))


def parse_issues(raw, option):
    """Parse comma-separated issue numbers; never echo the rejected value."""
    tokens = [t.strip() for t in raw.split(",")]
    if not all(re.fullmatch(r"#?[1-9]\d*", t) for t in tokens):
        raise SystemExit(f"invalid {option}: expected comma-separated issue numbers such as 12,34")
    return {int(t.lstrip("#")) for t in tokens}


def validate_evidence(active, inactive, issues):
    both = sorted(active & inactive)
    if both:
        raise SystemExit(f"--active and --inactive both name issues {both}")
    state = {i["number"]: i["state"] for i in issues}
    for option, nums in (("--active", active), ("--inactive", inactive)):
        bad = sorted(n for n in nums if state.get(n) != "OPEN")
        if bad:
            raise SystemExit(f"{option} names issues that are not open in {REPO}: {bad}")


def desired_status(state, current, has_open_pr, confirmed_active, confirmed_inactive):
    """Return (want, kept_unverified). Only per-issue evidence changes In Progress."""
    if state == "CLOSED":
        return "Done", False
    if has_open_pr or confirmed_active:
        return "In Progress", False
    if current == "In Progress" and not confirmed_inactive:
        return "In Progress", True
    return "Todo", False


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--active", help="open issue numbers with a coordinator-confirmed live session or frozen unpublished candidate")
    ap.add_argument("--inactive", help="open issue numbers expressly confirmed to have no live session and no frozen candidate")
    args = ap.parse_args()
    active = parse_issues(args.active, "--active") if args.active is not None else set()
    inactive = parse_issues(args.inactive, "--inactive") if args.inactive is not None else set()

    fields = gh_json("project", "field-list", str(PROJECT), "--owner", OWNER, "--format", "json")["fields"]
    status = next(f for f in fields if f["name"] == "Status")
    opt = {o["name"]: o["id"] for o in status["options"]}
    project_id = gh_json("project", "view", str(PROJECT), "--owner", OWNER, "--format", "json")["id"]
    items = gh_json("project", "item-list", str(PROJECT), "--owner", OWNER, "--limit", "1000", "--format", "json")["items"]
    board = {i["content"]["number"]: i for i in items if i["content"].get("number")}
    issues = gh_json("issue", "list", "--repo", REPO, "--state", "all", "--limit", "1000", "--json", "number,state,title,body,url")
    open_prs = gh_json("pr", "list", "--repo", REPO, "--state", "open", "--limit", "200", "--json", "number,title,body,headRefName")
    merged = gh_json("pr", "list", "--repo", REPO, "--state", "merged", "--limit", "1000", "--json", "number,title,body")

    def refs(prs):
        found = {}
        for pr in prs:
            text = f"{pr['title']} {pr['body'] or ''} {pr.get('headRefName', '')}"
            for num in set(re.findall(r"#(\d+)|issue-(\d+)", text)):
                n = int(num[0] or num[1])
                found.setdefault(n, []).append(pr["number"])
        return found

    open_ref, merged_ref = refs(open_prs), refs(merged)
    validate_evidence(active, inactive, issues)
    review, unverified = [], []

    for issue in sorted(issues, key=lambda i: i["number"]):
        n, body = issue["number"], issue["body"] or ""
        current = board.get(n, {}).get("status")
        if issue["state"] == "CLOSED":
            want = "Done"
            if UNTICKED.search(body):
                print(f"#{n} closed: tick criteria")
                if args.apply:
                    gh("issue", "edit", str(n), "--repo", REPO, "--body-file", "-", data=UNTICKED.sub(r"\1[x]", body))
        else:
            want, kept = desired_status(issue["state"], current, n in open_ref, n in active, n in inactive)
            if kept:
                unverified.append(n)
        if issue["state"] == "OPEN" and "epic" not in issue["title"].lower() and n in merged_ref and UNTICKED.search(body):
            review.append(n)
        if current == want:
            continue
        print(f"#{n} {issue['state'].lower()}: board {current or 'missing'} -> {want}")
        if not args.apply:
            continue
        item = board.get(n, {}).get("id")
        if not item:
            item = gh_json("project", "item-add", str(PROJECT), "--owner", OWNER, "--url", issue["url"], "--format", "json")["id"]
        gh("project", "item-edit", "--project-id", project_id, "--id", item,
           "--field-id", status["id"], "--single-select-option-id", opt[want])

    if unverified:
        print(f"activity unverified (kept In Progress: no open PR and no --active or --inactive evidence): {unverified}")
    print(f"review needed (merged PRs reference them, criteria unticked): {sorted(review)}")


if __name__ == "__main__":
    main()
