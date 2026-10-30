---
title: Resident browser check 571 changes
description: Implementation, validation and local delivery evidence
ms.date: 2026-10-30
---

## Context and Scope

Task 571 / resident-browser-check-571. Execute P01 then parent-owned P02
Review/local delivery. Plan and phase details share this slug under dated
plans/details paths. Research C1-C8 identifies stale check inputs; product
grammar remains unchanged. One critique executed, original Revise preserved;
PC-001 disposition recorded in plan. No blocker.

## P01 Implementation

P01-T01 implemented in `src/api/checks/resident_assistant_browser_check.py`:
supported document/form questions; explicit natural protected-route questions;
typed `ask_chat` waits for HTTP 200 and exactly one new assistant article.
Topic/document text and rules labels, document-source geometry and second
resident's absent-document facts bind to fresh replies. No runtime change or
acceptance assertion removed. Validation pending.

P01-T02 implemented: existing real HTTP document test now subtests each
supported question, exact document route and disabled-AI rules label alongside
unchanged facts/source/authority/isolation assertions. Two new methods cover
the exact browser form question and obsolete-prompt host-owned refusals using
the existing no-model/no-accounting/no-token helper. Addition cap respected.
P01-T03 guide updated with exact supported/refused questions and fresh-reply
acceptance rationale. Product and knowledge-base copy unchanged.

## Validation

Original untouched Chromium reproduction failed at the expected `Survey:
Missing` assertion on `documents help`. Original output retained at
`/tmp/ama-571-resident-baseline.log`. Existing accepted-document HTTP test
passed. Task-owned venv `/tmp/ama-571-venv` contains installed local editable
distributions and manifest dependencies; shared `/tmp/mv` was not changed.
All P01 required checks completed. Captured original output, log SHA-256
identities and browser summary are in
`.copilot-tracking/changes/2026-10-30/resident-browser-check-571-evidence.json`.

All commands below run from `src/api` using the task-owned interpreter/tools,
with `PYTHONDONTWRITEBYTECODE=1` and
`PYTHONPATH=tests:../core/tests:../agents/tests` for Python suites:

| Command | Outcome | Original external evidence |
| --- | --- | --- |
| `python -m checks.resident_assistant_browser_check --axe /tmp/ama-520-axe-4.10.3.min.js --out /tmp/ama-571-resident-baseline` (before source edits) | Failed exactly at line 330 on `Survey: Missing`; refusal to `documents help` | `/tmp/ama-571-resident-baseline.log` |
| Same command, `--out /tmp/ama-571-resident-green` | Passed actual loopback Chromium 156.0.8078.4; 32 axe states; no JS errors/external requests | `/tmp/ama-571-resident-green.log`, `/tmp/ama-571-resident-green/report.json` |
| `python -m unittest test_resident_chat_api -q` | Passed, 27 tests | `/tmp/ama-571-chat-units.log` |
| `python -m unittest discover -s tests -p 'test_resident*.py' -q` | Passed, 154 tests, seven opt-in skips | `/tmp/ama-571-resident-units.log` |
| `ruff check . && ruff format --check . && mypy` | Passed; 59 formatted files, 114 typed source files | `/tmp/ama-571-static-final.log` |
| `flock -w 600 /tmp/ama-rpi-heavy.lock /tmp/ama-571-venv/bin/python -m unittest discover -s tests -q` | Passed, 1363 tests in 482.777s, 318 skips; flock held for whole Python execution | `/tmp/ama-571-api-units.log` |

Resident skips: six opt-in isolated local SQL and one opt-in rendered browser.
Full discovery's 317 declared skips (collection inspected without executing
the suite again): 201 SQL Server, 50 disposable SQL, 36 owned MSSQL, 11 loopback
SQL, seven loopback MSSQL, six isolated resident SQL and six browser journeys.
One dynamic JSON skip excludes a SQL COMMIT acknowledgement boundary, as
declared in `test_progress_report_api.py`. These are explicit non-executions,
not successful SQL/browser integration results. The requested standalone
browser ran separately, not skipped.

### P01-T03 adversarial browser probe

Executed actual fixture/browser check under an in-memory routing fault. First
document answer succeeds, second identical document question is forced to
refuse. The revised check fails on its fresh `.nth(6)` assistant article even
though an earlier answer contains `Survey: Missing`. Expected failure observed,
probe exit 0 only after verifying that exact failure. No runtime source file
was modified. Original output: `/tmp/ama-571-resident-negative.log`.

Reproduce from `src/api`, with the same Python environment:

```python
import sys
from unittest.mock import patch
from checks import resident_assistant_browser_check as check
from zava_forward.api.resident_demo import chat

original = chat.route
calls = 0

def regress(question: str):
    global calls
    if question == "Which documents are missing from my case?":
        calls += 1
        if calls == 2:
            return "unknown"
    return original(question)

sys.argv = [
    "resident-negative", "--axe", "/tmp/ama-520-axe-4.10.3.min.js",
    "--out", "/tmp/ama-571-resident-negative",
]
try:
    with patch.object(chat, "route", side_effect=regress):
        check.main()
except AssertionError as error:
    assert calls == 2, calls
    assert "Locator expected to contain text 'Survey: Missing'" in str(error)
    assert "I cannot answer that" in str(error)
    print("EXPECTED FAILURE: second document reply refuses despite earlier successful document facts")
    print(error)
else:
    raise AssertionError("Resident check accepted a document regression using stale history")
```

### Scoped web-guideline/content review

Fresh guidelines fetched before review from the skill's official source on
2026-10-30. No production web files changed; changed Python harness, test and
API guide read against all applicable content and interaction rules. No new
UI-rule findings. Repository ASCII/sentence-case content rules take precedence
over generic curly-quote/title-case advice. Existing native semantics, focus,
manual routes and labels remain tested, not redesigned. Rules fallback remains
rules-labelled; no model-generated reply is recast as approved.

## Amendments and Divergences

None to product scope or acceptance. Parent may use external scratch and
user-required lock; independent critique's worker-local path restriction is
not a parent execution restriction. Do not recast its original verdict.

## Review and Remaining Work

P01 complete. P02-T01 single independent Review executed and original outcome
preserved at
`.copilot-tracking/reviews/logs/2026-10-30/resident-browser-check-571-review.md`:
Conformant within scoped correction, no implementation defects. Reviewer
checked captured-output hashes, AST, diff hygiene and source meaning without
claiming independent reruns. Low residual RV-001 (existing human/live
acceptance) and RV-002 (future publication gates) remain with relevant owners.
No material findings or current correction blockers. No source changes after
the assessed boundary; only parent-owned tracking reconciliation.

P02-T02 local Refs-only commit pending. Full publication gate, human acceptance
and hosted approval not claimed. No remote writes performed.
