#!/usr/bin/env python3
"""Audit and repair the GitHub backlog against the project board.

Default is a read-only audit. Use --apply to write. Rules:

* Closed issue: board Done and every acceptance checkbox ticked.
* Open issue on the board as Done: back to Todo (criteria are unmet).
* Open issue In Progress with no open PR and no live worktree: Todo.
* Open issue Todo with an open PR that references it: In Progress.
* Issue missing from the board: added with the status implied above.

Open issues with merged PR references but unticked criteria are listed for
human or coordinator review because criteria need evidence to be ticked.
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


def live_worktree_issues():
    out = subprocess.run(["git", "worktree", "list", "--porcelain"], capture_output=True, text=True).stdout
    return {int(m) for m in re.findall(r"^worktree .*issue-(\d+)$", out, re.M)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

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
    live = live_worktree_issues()
    review = []

    for issue in sorted(issues, key=lambda i: i["number"]):
        n, body = issue["number"], issue["body"] or ""
        current = board.get(n, {}).get("status")
        if issue["state"] == "CLOSED":
            want = "Done"
            if UNTICKED.search(body):
                print(f"#{n} closed: tick criteria")
                if args.apply:
                    gh("issue", "edit", str(n), "--repo", REPO, "--body-file", "-", data=UNTICKED.sub(r"\1[x]", body))
        elif n in open_ref or n in live:
            want = "In Progress"
        else:
            want = "Todo"
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

    print(f"review needed (merged PRs reference them, criteria unticked): {sorted(review)}")


if __name__ == "__main__":
    main()
