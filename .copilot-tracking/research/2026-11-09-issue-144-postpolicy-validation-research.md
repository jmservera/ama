# Research: issue 144 post-policy validation of the queue request-date fix (2026-11-09)

Task: `issue-144-postpolicy-validation-2026-11-09`. Parent: `issue-144-queue-request-date-c1-2026-11-09`. Research disposition: executed (target/base comparison) plus reused (C1 research for the Azure Date contract). Planning Readiness: Ready.

## Scope

Fresh selected-tier validation and target-base evidence for the already independently approved Date/`x-ms-date` correction before any forward publication. No source change is intended. All earlier adverse records stay unchanged: original review in `.copilot-tracking/reviews/2026-11-09/issue-144-independent-functional-review/` and the C1 self review. Not evidence for acceptance: the old green hosted CI on PR 1141 or any old receipt.

## Identities (read-only, fetched 2026-11-09)

| Item | Value |
| --- | --- |
| Frozen candidate HEAD | `63d7f8c180ee995121144cf593e8eca7cb94bd4d`, tree `f08a112691ed6658a881f932f1ca2f3f71396837` |
| Independently approved exact head (coordinator report `independent-144-c1`) | same SHA, verdict approve, original finding 1 closed |
| Previous base | `b46a9ad9a9619db535368d1b2cbbddec8110e122` (merge-base of HEAD and current main) |
| Current `origin/main` | `9814cf6b236be1f2e86c4401973b8e834be927bc` (#1301, after #1294 closed with all five criteria) |
| PR 1141 | open, base `main`, head `feat/slice-144` at `1a9616d4e9ab89d93a72204d82ee26c70baee06c`, 18 checks SUCCESS and 1 with no conclusion, mergeability `UNKNOWN` |

## Findings

1. Main moved one commit past the previous base: `git rev-list --count b46a9ad9..origin/main` is 1 (#1301, "docs(validation): streamline local checks while preserving coverage").
2. That commit changes 91 paths, all under `.copilot-tracking/`, `docs/`, `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `.github/copilot-instructions.md`, `.github/rubric/README.md` and `src/README.md`. No path under `src/agents`, `src/core`, `src/api`, `src/orchestrator`, `src/importer`, `tools/`, `infra/`, `.github/workflows/`, or any `pyproject`, requirements, lock or Dockerfile file changed.
3. Overlap with the candidate diff since the base is one path, `docs/reference/log.md` (append-only log; both sides appended).
4. `git merge-tree --write-tree HEAD origin/main` exits 0 with tree `985d09b2892aa3aec8b634ee922f9e6ba4823e09`. The source, tools, infra and workflow paths of that tree are identical to HEAD. The old remote head `1a9616d4` is an ancestor of HEAD (80 commits behind) and also merges cleanly into main. No rebase or merge is needed to preserve ancestry; the actual relation is recorded, not changed.
5. The remote branch `feat/slice-144` was fetched only; it was not moved.
6. New policy (`.github/copilot-instructions.md`, #1294): small issues take the focused tier of planned relevant local checks plus hosted CI for the exact head; a blanket `rpi-checks --changed` is optional and never replaces planned checks; absent, path-filtered or unobserved hosted workflows are not successes. Owner demo tier (brief, 2026-11-09) additionally replaces the full gate for this demo push. Classification: the candidate adds one header to a Python client, with unchanged `Authorization`, no workflow, dependency, image, permission, secret or gate change, and no SQL. Tier: focused/demo-targeted. Basis recorded in the plan.
7. Azure Date contract (reused from C1 research, Microsoft Learn Get Messages header table, page updated 2023-06-27, checked 2026-11-09): "Date or x-ms-date: Required". The correction sends `x-ms-date` with `email.utils.formatdate(usegmt=True)` per request.
8. Existing tools: venv `/tmp/c1venv` survives; editable installs resolve to this worktree (`zava-forward-core` and `zava-forward-agents` at `/home/azureuser/source/ama-demo-wt/issue-144/src/...`); ruff 0.17.1 and mypy 2.4.0 are present. No install is needed.
9. The suite named by the owner has 49 cases across `test_queue_azure` (24), `test_worker`, `test_dispatch` and `test_dependency_rule`. Bare `unittest discover` needs the README helper `PYTHONPATH` and is not used.

## Issue 144 criteria

All five stay unchecked on the evidence available: real images, deployed hardening, load test and restart/audit persistence need Azure and are not claimed. The offline queue proof does not close or tick any criterion; the PR uses `Refs #144`.

## Gaps and limits

* Hosted CI for the exact local head is unobserved (head is not pushed). Old PR checks are not evidence for it.
* No Azure request is made; the 403 behaviour is a local transport that mimics the documented requirement.
* Independent review is of the exact head `63d7f8c1`; any new commit holding only these validation records needs the reviewer to confirm that source and tests are unchanged.
