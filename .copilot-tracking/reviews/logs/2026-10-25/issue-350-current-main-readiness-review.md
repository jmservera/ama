<!-- markdownlint-disable-file -->
---
title: Issue 350 current-main readiness review
description: One scoped independent assessment of the main merge, retained checker contracts and RV-201; outcome preserved
ms.date: 2026-10-25
---

Execution: complete, once, read-only `rubber-duck`, after the pre-merge critique (Revise, corrected at execution), the merge and the focused tests. Outcome: **non-conformant**. It is preserved and not relabelled. No second assessment was run, and the corrections below were not independently re-verified.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| RV-301 | Reported blocking | Merge first parent is `ec9d4d92`, not `a9bdae31`. | Explained, not a defect: my assessment brief wrongly named a9bdae31 as the first parent. `ec9d4d92` is the committed readiness plan, research, details and critique, made before the merge, and a9bdae31 is its parent. The reviewer confirmed a9bdae31, origin/main and the remote branch are all ancestors. |
| RV-302 | Blocking | The critique said PC-301 was applied, but the plan and details were not amended and still read conditionally. | Critique disposition corrected to disclose that the stricter procedure was applied at execution only. Plan and details are left as written. |
| RV-303 | Non-blocking | "Store unchanged" was too broad; main changed `sqlstore.py` and `seed_merge.py`. | Wording narrowed in the critique. |
| RV-304 | Non-blocking | Diff from a9bdae31 includes four branch-owned readiness artifacts besides main-owned files. | Accounted for here. Expected diff is main-owned files plus those four artifacts, and now this review, changes and state records. |

Confirmed by the reviewer: ancestry of a9bdae31, `origin/main` ea5577b2 and the remote branch; `RecursionError` handling at `tools/check-demo-feedback.py:118` and the Application Administrator validation at :226-259; the deep-nesting and admin-only regression tests present; plan commit precedes the merge (same minute, so timestamps alone give topological order only).

RV-201 re-verification: the corrected PC-201 wording in the retry critique is accurate against git history (a9bdae31 added the retry artifacts after 16e6d12d), and the disclosure in the retry review is honest. This re-verifies the wording correction only. It does not accept the retry review, which stays non-conformant, and overall acceptance remains an owner or coordinator decision.

Focused checks, fresh venv from `git archive` of the merged HEAD (package paths under `/tmp/c2-350/v/.../zava_forward`, then deleted): `tools.test_check_demo_feedback` 80 OK including `test_runtime_admin_only_response_passes_without_acceptance`, `test_admin_payload_rejects_business_data_or_missing_flag` and `test_excessive_json_nesting_is_blocked_not_raised`; `src/core` `test_seed_merge.py` via discover 21 OK (a direct `unittest tests.test_seed_merge` fails to import `dataset`, a runner-path artefact, not a code fault). No source change was made. No Docker, SQL service, gate, push, PR or issue edit. Original 2026-10-24, 2026-10-25 and retry reviews are unchanged.
