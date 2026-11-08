---
title: Issue 1231 research r2 (owner-approved hard-link contract verification)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Written 2026-11-06 about 07:58Z, before any source, test or documentation edit and before any new probe or test run in this continuation. Same original session b353a2c9, same task lineage. The R1 research, plan, details, changes, review, state and external raw outputs (`/tmp/1231-ranking-archive-r1-1106/`) are preserved unchanged, including the R1 qualifications that the owner question was open, that the process test does not force an interleaving, and that overwrite of a finished record was never demonstrated.

## Identity and pins

* Branch `fix/ranking-archive-concurrent-writer-metadata`, head `57b3b6a09f6ac5b77b37881e21447751a56be5ff`, tree `fea8273a05c2a42da3e127d77a2c4ad9377f365b`, ignored-inclusive status empty at intake.
* Parent #79 `feat/ranking-publication-runner-79` at `397419724e68b24bce879512a24c7df430177f87` (local only); grandparent #73 `feat/case-workbench-integration-73`. Eventual PR targets the #79 parent, not main. Read-only fetch resolved `origin/main` to `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` (provenance only). No branch moved, rebased or merged.
* Research disposition `executed`; Planning Readiness `Ready`.

## New owner decision (verbatim, as relayed)

"Yes - Require atomic hard links and fail closed otherwise (recommended)" (the actual form used a Unicode dash). It approves the archive filesystem compatibility requirement for #79 and #1231: unsupported filesystems must explicitly refuse publication, with no unsafe overwrite and no silent fallback. It resolves the R1 owner compatibility question. It does not approve deployment or mount changes, retention or legal decisions, operational policy ownership, publication, paid calls or cloud activity. R1 recorded this as an open question; that point-in-time record stays as written.

## Existing implementation (read, R1 head)

`ranking_publication.publish`: validate, `makedirs`, exists pre-check returning `_existing` (written False), unique exclusive stage `.<name>.<hex>.tmp`, write canonical text, `os.link(stage, final)`; `FileExistsError` returns the finished record with `written=False`; any other `OSError` propagates; `finally` unlinks only the owned stage. Runner turns `OSError` into `publish_failed`. Docstring and README already state the hard-link requirement and refusal.

## Verification questions for this continuation

1. Is an unsupported-hard-link refusal explicit and tested? Existing test injects `PermissionError` at `os.link`; no test uses a hard-link-unsupported errno (`EPERM`/`ENOTSUP`/`EOPNOTSUPP`) or checks the runner refusal. Propagation is by construction. Unknown whether the stage cleanup, no-record and runner `publish_failed` refusal (code, message, next action) are asserted for that class.
2. Is there a silent fallback? By reading none: only `FileExistsError` is caught. Gap candidate: a stage with a failing `os.unlink` in `finally` could mask the original error; reasoned only.
3. Truthful winner metadata, immutable existing records, owned-only cleanup: covered by R1 tests (read, to be re-run).
4. Coupled gap candidates: runner-level refusal for unsupported hard links; the runner message text "Check the archive location and rerun." does not mention hard links. A correction is not assumed; it is made only if a regression demonstrates an actual gap, and kept minimal.

## Limits carried forward

Light only: no FULL, SQL, browser, container, scan, heavy lock or queueing. `/tmp/zf79venv` is read-only; tools there are ruff 0.17.3 and mypy 2.4.1 against the project pins ruff 0.17.1 and mypy 2.4.0, so results are not isolated-package or FULL evidence. Windows, network filesystem and production unmeasured; no deployment, mount, retention or approval is decided.
