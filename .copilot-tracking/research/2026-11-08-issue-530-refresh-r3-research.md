---
title: Issue 530 focused-gate refresh r3 research
ms.date: 2026-11-08
---

* Task: `issue-530-refresh-r3`, continuation of `issue-530-chat-local-unit` and `issue-530-focused-gate-admission-prep`. Research disposition: executed (read-only). Planning Readiness: Ready.
* Start: HEAD `1a25d082f60843148af6a10c83f87df31789b8e1`, tree `9f27a90cca28bf32e446bf1118093adb8679b8b8`, ignored-clean. Fetched `origin/main` `2e0c676ada9264b4322224a24bc98aa3367d4f4a`, tree `08f9a4f995a0a50f58b2a319618666c8c704ada9` (rubric bot commit on merged #1268 `4194c49e`).
* Preserved: the 4194 refresh stopped on drift with no records, merge, gate or output; r1 receipt `d619ea82...` is immutable, passed for old base `f548b65f`, and now fails verification ("Base moved on src/api/tests/assistant_process_worker.py"), recorded as BLOCKED, not BASE_RELAXED. No `--resume`.

## Findings

* Selection logic: `selection()` computes `git diff --no-renames --name-only -z <base>...HEAD` (three-dot: changes on HEAD since the merge base). Commits reachable from the base, such as an incoming Main merge, are never in that set once the base is an ancestor of HEAD. The earlier pre-merge `HEAD...origin/main` listing (rubric JSON, `assistant_process_worker.py`, `test_assistant_release.py`) is incoming Main content, not a candidate change.
* After a normal merge of `2e0c676a`, the merge base of `2e0c676a` and the new HEAD is `2e0c676a`, so the set equals the candidate-only paths: the inert `.copilot-tracking/` records. `changed_groups` skips inert paths (`inert_path`: `.md` or prefixes `docs/`, `.copilot-tracking/`, `support/`), so `.github/rubric/scores/latest.json` does not select FULL once it is in the base. The non-inert branch (`required_groups`, full matrix) fires only for a non-inert path in the post-merge set.
* Expected selection: `preflight`, `namespace`, `static`; the same skip set as r1 (five projects, infra, migration, browser, mssql, four images, logo-0600). The real `groups=` line must match.
* Same-source attribution: the original 71 chat units ran on blobs of `ed19cb94`. Main's incoming test changes touch `assistant_process_worker.py` and `test_assistant_release.py`, not the selected chat modules. The post-merge blobs of the six selected chat test files and `src/core`, `src/agents` trees must be compared with the original (see details); if they differ, attribution is reported as not qualified.
* Lock: the canonical lock file exists as a path; actual holder is checked by the runner (`--lock-timeout 0`), no polling.
* Identity: authenticated `jmservera` id 8036360.

## Evidence boundary

Read-only so far. No SQL, browser, live or human acceptance is claimed; those #530 criteria stay unmet.
