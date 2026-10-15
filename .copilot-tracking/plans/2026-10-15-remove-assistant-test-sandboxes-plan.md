---
title: Plan - remove assistant test sandboxes
---

* [x] `git rm` the tracked `mvp/.assistant-test-*/` directories.
* [x] Create the sandbox with `tempfile.mkdtemp` outside the repository and register `addCleanup(shutil.rmtree)` so cleanup runs even if `setUp` fails.
* [x] Add `/mvp/.assistant-test-*/` to `.gitignore`.
* [x] Add a CI step in `mvp-ci.yml` that fails when tracked files match `mvp/.assistant-test-*` (a CI step keeps the test count at 719).
* [x] Validate: unit tests pass with 719 tests and a clean `git status`.

Critique (single pass): the sandbox must be removed on failed setUp as well as teardown, so cleanup is registered immediately after creation. Applied.
