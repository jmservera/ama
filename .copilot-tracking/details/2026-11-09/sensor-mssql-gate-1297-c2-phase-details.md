---
title: Phase details - #1297 correction C2
date: 2026-11-09
---

## P01 Apply pinned formatter and validate

* P01-T01: run `/tmp/ruff1297-c2/bin/ruff format --isolated --line-length 100` on tools/rpi-checks.py only. Evidence: research C1-C3.
* P01-T02: validate with pinned ruff format check, lint (E,F,I,B,UP, py312, line length 100), `mypy --strict` with external cache, and `cd tools && python3 -m unittest test_rpi_checks` with PYTHONDONTWRITEBYTECODE=1. Test ownership: none added or removed.
