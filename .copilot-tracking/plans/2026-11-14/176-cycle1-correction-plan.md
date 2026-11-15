# #176 Cycle 1 correction plan (2026-11-14)

1. `build(out_dir, seed=444, as_of=None)`: pin the clock and id sources while building; default `as_of` 2026-10-24; record seed, version, as_of, generator_revision in `dataset.json` `synthetic_preview`.
2. Add `generator_revision` to the fault-mode `truth/manifest.json`.
3. API `--as-of` option (default today); tests pass `as_of=date.today()`.
4. Extend `test_generator_determinism_matrix.py`: clock-guarded preview replay across hash seeds, and fault-rates revision.
5. Run focused tests, ruff and mypy on touched files. Critique: none required (small, compatible fixes).
