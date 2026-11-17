---
title: "Issue 1297 gate bytecode hygiene details"
ms.date: 2026-11-16
---

## Phase 1

Add `test_every_venv_install_prevents_scrubbed_child_writing_source_bytecode` near the existing api test. For each of `core`, `agents`, `orchestrator`, `importer`, `namespace`: run `runner._install(name, [...])` with `command` patched to create the venv with `--without-pip`; make a temporary module under a scratch dir; run `[interpreter, "-c", "import mod"]` with `env={"PATH": ..., "PYTHONPATH": scratch}` (no bytecode variables); assert no `__pycache__`/`.pyc` in scratch. Also assert the venv `.pth` content.

## Phase 2

`_install`: replace `if name == "api": self.install_bytecode_policy()` with an unconditional venv `.pth` write; the `out/browser-bytecode-policy.pth` write stays for `api` so `required_files` is unchanged. Comment: scrubbed children (browser harness servers, discovery demo test) drop the Runner flags (#1215, #1297).

## Phase 3

`python3 -m unittest` for `tools/test_rpi_checks.py` (targeted names, then module), ruff format --check and check on the two tool files with the pinned version the gate uses.
