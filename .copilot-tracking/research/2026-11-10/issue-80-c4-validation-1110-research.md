---
title: Issue 80 capacity C4 instrumented validation, research
description: Research for one observed whole capacity_browser_check --axe execution on unchanged source 2cc34027
ms.date: 2026-11-10
---

## Scope and disposition

* Task `issue-80-c4-validation-1110`, parent `issue-80-capacity-c4-1110`. Source pin: clean HEAD `2cc340270b5fca04d8374f334a4a9fd6dc94a8e9` (tree `b41c022b40b48be45f94ef90a079a53cdc470147`), main `6d4cd624` (contained, not re-fetched). Research disposition `executed` (source reading of the checker harness and Playwright hook points).
* Root admits ONE instrumented whole `capacity_browser_check --axe` execution on UNCHANGED application and checker source. This is a validation admission, not a source correction and not C5. No source, test or fixture edit, no further isolated probe, no repeat after red. It replaces the earlier C4 "whole run only after cause" restriction for this execution only.
* Open and unchanged: C4-R1 (no runtime proof), C4-R2 (initial 503 failure at line 571 unexplained), original C4 review, C1 batched implement-start preflight, C2 early review draft (sha256 `191d1caa...cf570`), C3 adverse run and review.

## Budget disclosure (prior C4)

* The C4 research ran TWO driver commands but SEVEN scenario observations (the second driver looped six iterations). The admitted limit was two observations, not two commands. All seven are preserved. This is a deviation, not strict compliance, and is not reset, debited or rerun.

## Harness facts (source read)

* `main()` (about line 920) clears the environment to PATH, HOME, TMPDIR, LANG and LD_LIBRARY_PATH, takes `/tmp/ama-rpi-heavy.lock` with `LOCK_NB` (BLOCKED exit on busy, no wait), builds a synthetic seed under a temp directory and calls `check(store, axe)`. `ZF_DATA` is therefore absent from the run environment.
* `check()` builds a loopback `ThreadingHTTPServer` and one Chromium context with a `**/*` route that continues only the loopback origin and aborts the rest. `scenario` progress is reported through module-level `print(..., flush=True)` calls.
* The browser is closed in a `finally`, so a failing `expect` timeout leaves no live page for an outer handler. The `Browser.close` call happens while the primary exception is in flight (`sys.exc_info()` set), which lets an observer snapshot the page before closing.

## Observer design (external, passive)

* File `phase80-capacity-c4-validation-evidence-1110/observer.py` (sha256 recorded in `observer.py.sha256`), run with the owned venv. It imports the unchanged checker and calls its `main()`.
* Passive context listeners only: request, response, requestfailed, console, pageerror, and main-frame navigation. It records time, method, URL path with only `limit` and `offset` paging keys, status, response content type, pending request count and console or page error text (200 chars). It records no request headers, no cookies, no bodies.
* A module-level `print` shadow in the checker namespace records each milestone with the caller line and then calls the real print, so checker output is unchanged.
* Wrappers on `Browser.new_context`, `BrowserContext.new_page` and `Browser.close` attach listeners and take one DOM snapshot (hash, ready state, alerts, statuses, heading, busy count, app text prefix, pending paths) at close. After the snapshot it fetches each served asset path once and compares the sha256 with the owned `web/` files, then closes.
* `check` is wrapped to log the store type and path strings, assert `ZF_DATA` absent, and record the primary exception type, message and last frames before re-raising it unchanged. `main` is wrapped so the exit code is recorded and re-raised exactly. Observer faults are caught, logged as `observer_error` and never raised.
* Origins recorded: checker, server, sqlstore, generated-dataset and fixtures module files, the checker sha256, installed distribution versions and owned web file hashes.

## Observer limitations (exact)

* Listeners and the print shadow add small synchronous work in the Playwright dispatcher and the checker thread; this is not zero cost and its effect on timing is unmeasured. Each event is one `write` plus `flush`, with no `fsync`, so a host crash can lose the tail but a process failure cannot.
* Route handler matching is internal to the checker and is NOT directly observable. Which handler served a request is inferred from the response status and timing only. Held (not yet released) responses show as requests without a response and in the pending list.
* Playwright events may be delivered after the corresponding DOM change, so event order across request and DOM is approximate.
* Timers are not instrumented, disabled or fast-forwarded. Retry timing is read from request timestamps only.
* The failure snapshot is taken in `Browser.close`, after the expect timeout elapsed, so it shows the state at close, not at the first moment of failure.
* The served-asset comparison covers only paths requested as non-API; the HTML shell may not equal an owned file byte for byte, which will be reported as no match, not as a defect.
* A whole run is a single sample. A pass does not prove stability; a failure may be host load, a checker race or an application defect, and the observer cannot decide that.

## Evidence plan

* Pre-run: confirm clean tree, HEAD and file hashes equal the pins, host load noted, venv imports resolve to owned `src/` distributions, lock not held by this author.
* One execution under `PYTHONPATH` as in prior chains, with direct Python exit captured as `$?` of the python process itself (output to a file, no pipe).
* Carried evidence: API11, static60, Ruff and Node from the C4 commit on the same source (hashes unchanged); not re-run, no new tests.
